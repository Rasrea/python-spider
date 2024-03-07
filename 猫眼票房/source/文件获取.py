from 字体破译 import beat_data
from 破译票房 import get_boxs
from 简单数据 import simple_data
import os
import requests
import time
from selenium import webdriver
from fontTools.ttLib import TTFont


# 获取字体和数据文件，并转换字体文件，读取数据文件
def get_files():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/121.0.0.0'
                      'Safari/537.36'
    }
    love_day = input('请输入查找日期（如1314-05-21）：')  # 自定义查找日期

    # 启动Chrome浏览器，需要安装ChromeDriver，以调整环境变量
    driver = webdriver.Chrome()

    # 打开网页
    print('休息一会儿，等待网站加载\n')
    driver.get(f'https://piaofang.maoyan.com/dashboard/movie?date={love_day}')

    # 等待一段时间以确保页面加载完成
    time.sleep(4)

    # 获取网页中的所有woff文件
    woff_urls = set()
    for entry in driver.execute_script('return window.performance.getEntries();'):
        if entry.get('name') and entry.get('name').endswith('.woff'):
            woff_urls.add(entry['name'])

    # 检查是否找到了woff文件的URL
    if not woff_urls:
        print('数据太过久远或网络出差，请重试！！')
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

    # 读取数据，防止后续更新
    xhr_data = requests.get(xhr_url, headers=headers).json()
    movie_list = xhr_data['movieList']['list']
    # 转换成xml格式，便于破解
    font = TTFont(font_filename)
    font.saveXML(font_filename + '.xml')
    xml_file = font_filename + '.xml'
    print("字体文件格式转换完成！\n")

    # 破译数据并读取数据
    key_dict = read_xml(xml_file)  # 读取XML，破解加密数据
    combine_money, part_money = get_boxs(key_dict, movie_list)  # 破译票房信息
    simple_data(movie_list, combine_money, part_money, love_day)  # 爬取简单信息


# 读取XML，转化加密数据
def read_xml(xml_file):

    with open(xml_file, 'r') as file:
        xml_text = file.read()
    key_dict = beat_data(xml_text)  # 破译字体文件函数
    return key_dict
