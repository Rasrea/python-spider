import os
import requests
import time
import re
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from fontTools.ttLib import TTFont

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 '
                  'Safari/537.36'
}


# 破译字体文件
def beat_data(xml_text):
    # 找出XML文件中的加密信息
    pattern = re.compile(r'<TTGl.*?name="(uni.*?)".*?xMin=.*?>(.*?)</TTGlyph>', re.S)
    image_text = re.findall(pattern, xml_text)
    # 将加密信息按字符'contour'个数分类
    two_count = []
    one_count = []
    key_thr = {}  # 以字典的形式存储破解信息

    # 循环遍历每个加密信息
    for i, str_text in enumerate(image_text):
        count_text = re.findall(r'<contour>', str_text[1])
        # 分别存放在各自的列表中
        if len(count_text) == 3:
            key_thr[str_text[0]] = 8
        elif len(count_text) == 2:
            two_count.append(str_text)
        else:
            if i == len(image_text):  # 排除最后一个
                break
            else:
                one_count.append(str_text)

    # 根据图像数据的行数进一步区分列表中的值
    line_dict = {}
    list_two = [9, 6, 0, 4]
    for data in two_count:
        line_count = data[1].count('\n') + 1
        line_dict[data[0]] = line_count

    # 使用sorted函数对字典的键值对进行排序，根据值进行排序，reverse参数设置为True表示降序
    key_two = dict(sorted(line_dict.items(), key=lambda item: item[1], reverse=True))

    # 使用循环遍历使解码结果分别对应4
    for key, value in zip(key_two.keys(), list_two):
        key_two[key] = value

    # 区分数字9和6，比较第二部分y坐标的大小
    # 获取字典的键列表
    keys = list(key_two.keys())
    nin_text = ''  # 初始化
    six_text = ''
    for text in image_text:
        if text[0] == keys[0]:
            nin_text = text
        if text[0] == keys[1]:
            six_text = text

    # 获得数字9第二部分y坐标值和
    sec_nin_text = re.search('</cont.*?tour>(.*?)</contour>', nin_text[1], re.S).group(1)
    nin_y = [int(i) for i in re.findall(r'y="(.*?)" on=', sec_nin_text)]
    # 同理得数字6
    sec_six_text = re.search('</cont.*?tour>(.*?)</contour>', six_text[1], re.S).group(1)
    six_y = [int(i) for i in re.findall(r'y="(.*?)" on=', sec_six_text)]

    # 比较第二部分y坐标的值的总和
    if sum(nin_y) < sum(six_y):
        # 9, 6需要调换
        keys = list(key_two.keys())[:2]  # 获取字典中的前两个键
        key_two[keys[0]], key_two[keys[1]] = 6, 9

    # 同理破译另一部分
    line_dict = {}
    list_one = [3, 2, 5, 7, 1]
    for data in one_count:
        line_count = data[1].count('\n') + 1
        line_dict[data[0]] = line_count
    key_one = dict(sorted(line_dict.items(), key=lambda item: item[1], reverse=True))
    for key, value in zip(key_one.keys(), list_one):
        key_one[key] = value

    # 合并成解码字典
    key_dict = {**key_thr, **key_two, **key_one}

    return key_dict  # 返回破译字符


# *******获取字体和数据文件********

# 设置Chrome浏览器选项
chrome_options = Options()
chrome_options.add_argument('--headless')  # 启用无头模式
chrome_options.add_argument('--remote-debugging-port=9222')  # 启用远程调试端口

# 启动Chrome浏览器，需要安装ChromeDriver，以调整环境变量
driver = webdriver.Chrome(options=chrome_options)

# 打开网页
print('休息一会儿，等待网站加载\n')
driver.get('https://piaofang.maoyan.com/dashboard/movie')

# 等待一段时间以确保页面加载完成
time.sleep(8)

# 获取网页中的所有woff文件
woff_urls = set()
for entry in driver.execute_script('return window.performance.getEntries();'):
    if entry.get('name') and entry.get('name').endswith('.woff'):
        woff_urls.add(entry['name'])

# 检查是否找到了woff文件的URL
if not woff_urls:
    print('网络加载过慢，请重试!!')
    driver.quit()
    exit()

# 获取最新的woff文件
latest_woff_url = max(woff_urls, key=lambda x: requests.head(x).headers.get('Last-Modified', 0))

# 发送GET请求以获取最新字体文件的内容
response = requests.get(latest_woff_url, headers=headers)
if response.status_code == 200:
    font_data = response.content
    # 提取字体文件名
    font_filename = os.path.basename(latest_woff_url)
    # 保存字体文件到本地
    with open(font_filename, 'wb') as f:
        f.write(font_data)
    print(f"最新字体文件 '{font_filename}' 下载成功！")
else:
    font_filename = ''
    print(f"无法下载最新字体文件 '{latest_woff_url}'，HTTP状态码：{response.status_code}")

# 获取网页中的所有请求
requests_data = driver.execute_script('return window.performance.getEntries();')

# 初始化内存最大的XHR文件信息
max_xhr_url = None
max_xhr_memory = 0

# 遍历所有请求，找到符合条件的XHR类型文件
# 要求内存最大、最新、含有字符串 'piaofang.maoyan.com'
for request in requests_data:
    if request.get('initiatorType') == 'xmlhttprequest' and 'piaofang.maoyan.com' in request.get('name'):
        request_memory = request.get('encodedBodySize', 0)
        if request_memory > max_xhr_memory:
            max_xhr_memory = request_memory
            max_xhr_url = request.get('name')

# 如果没有找到符合条件的XHR类型的文件，则退出程序
if not max_xhr_url:
    xhr_url = ''
    print('未找到符合条件的XHR类型的文件！！')
else:
    print('数据文件的URL：')
    xhr_url = max_xhr_url  # 获取数据文件
    print(max_xhr_url)

# 关闭浏览器
driver.quit()

# *******存储数据，防止更新*********

xhr_data = requests.get(xhr_url, headers=headers).json()
movie_list = xhr_data['movieList']['list']

# 转换成xml格式，便于破解
font = TTFont(font_filename)
font.saveXML(font_filename + '.xml')
xml_file = font_filename + '.xml'
print("字体文件格式转换完成！\n")

# *********读取XML，转化加密数据***********

with open(xml_file, 'r') as file:
    xml_text = file.read()
key_dict = beat_data(xml_text)  # 破译字体文件函数

# *********破译票房信息************

# 获取当前文件夹路径
folder_path = os.path.dirname(os.path.realpath(__file__))
# 获取当前文件夹中的所有文件，如果字体更新，则遍历其他字体
files = os.listdir(folder_path)

# 解析票房（综合及分账）数据
combine_money = []  # 存储综合票房
part_money = []  # 存储分账票房
for item in movie_list:
    # 初始化票房数据
    t_con_money = ''
    t_par_money = ''

    # 提取（综合）票房信息，转为大写、替换字符、转换成列表
    combine_text = item['boxSplitUnit']['num'].upper().replace('&#X', 'uni')
    combine_lst = re.findall(r'(uni.*?);', combine_text)  # 转化成列表，方便之后遍历
    # 提取（分账）票房信息，同上
    part_text = item['splitBoxSplitUnit']['num'].upper().replace('&#X', 'uni')
    part_lst = re.findall(r'(uni.*?);', part_text)

    # 如果字体文件与数据文件不匹配，则更改字体文件
    if not all(key in key_dict for key in combine_lst):
        # 过滤出 XML 文件
        xml_files = [file for file in files if file.endswith('.xml')]
        # 遍历字体文件，直达符合后返回
        for x_file in xml_files:
            with open(x_file, 'r') as f:
                xml_text = f.read()  # 读取数据后重新返回破译函数

            # 再次开始破译
            key_dict = beat_data(xml_text)
            if all(key in key_dict for key in combine_lst):
                break  # 如果字符全部匹配，则破译成功，返回破译字典

    # 遍历转换（综合）票房并存储
    for i in combine_lst:  # 将字符串相互对比、转化
        t_con_money = t_con_money + str(key_dict[i])
    t_con_money = float(t_con_money) / 100  # 保留两位小数
    combine_money.append(t_con_money)
    # （分账）票房同上
    for j in part_lst:
        t_par_money = t_par_money + str(key_dict[j])
    t_par_money = float(t_par_money) / 100
    part_money.append(t_par_money)

# ***********爬取简单信息*************

film_name = []  # 名称
release_time = []  # 上映天数
all_combine = []  # 总票房（综合）
all_part = []  # 总票房（分账）
show_rate = []  # 票房占比（综合）
split_rate = []  # 票房占比（分账）
show_count = []  # 排片场次
count_rate = []  # 排片占比
avg_show = []  # 平均场次
avg_seat = []  # 上座率

for lantern in movie_list:
    # 爬取上映天数
    t_time = lantern['movieInfo']['releaseInfo']
    if '天' in t_time:
        time = re.search('上映(.*?)天', t_time).group(1)
        release_time.append(time)  # 分离上映天数
    elif len(t_time) == 0:
        release_time.append('重映')  # 上映时间为空
    else:
        release_time.append(t_time)

    # 爬取总票房（综合及分账）
    all_combine.append(lantern['sumBoxDesc'])
    all_part.append(lantern['sumSplitBoxDesc'])

    # 爬取票房占比（综合及分账），并去除%
    show_rate.append(lantern['boxRate'].split('%')[0])
    split_rate.append(lantern['splitBoxRate'].split('%')[0])

    film_name.append(lantern['movieInfo']['movieName'])  # 爬取名称
    show_count.append(lantern['showCount'])  # 爬取排片场次
    count_rate.append(lantern['showCountRate'].split('%')[0])  # 爬取排片占比，并去除%
    avg_show.append(lantern['avgShowView'])  # 爬取平均场次
    avg_seat.append(lantern['avgSeatView'].split('%')[0])  # 爬取上座率，并去除%

# ***********导入csv文件*************

# 定义列名
headers = ['排名', '名称', '实时（综合）票房（万）', '实时（分账）票房（万）', '上映时间（天）',
           '总票房（综合）', '总票房（分账）', '综合票房占比（%）', '分账票房占比（%）',
           '排片场次', '排片占比（%）', '场均人次', '上座率（%）']

# 将列表按竖列写入CSV文件
with open('猫眼电影数据.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)  # 写入列名

    # 写入数据，并增加排名
    for i, row in enumerate(zip(film_name, combine_money, part_money, release_time,
                                all_combine, all_part, show_rate, split_rate,
                                show_count, count_rate, avg_show, avg_seat), start=1):
        writer.writerow([i] + list(row))

print('数据爬取完成！')
input('Please enter any keys to exit')
