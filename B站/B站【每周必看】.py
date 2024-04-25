import requests
import re
import pandas as pd
import time
import random
from datetime import datetime, timedelta
from tqdm import tqdm


# 计算时间，年月日（日取中值）
def scrape_time(s):
    result = re.search(r'(.*?)第(.*?)期(.*?-.*$)', s)
    time_str = result.group(3).strip().replace(' ', '')  # 去除空格
    # 分割字符串为两个日期
    start_date_str, end_date_str = time_str.split('-')
    # 添加年份
    year = result.group(1)
    start_date_str = year + '.' + start_date_str
    end_date_str = year + '.' + end_date_str
    # 将日期字符串转换为datetime对象
    start_date = datetime.strptime(start_date_str, '%Y.%m.%d')
    end_date = datetime.strptime(end_date_str, '%Y.%m.%d')
    # 计算两个日期的中间点
    mid_date = start_date + (end_date - start_date) / 2
    # 将中间点日期转换回字符串
    mid_date_str = mid_date.strftime('%Y.%m.%d')
    # 添加年
    mid_time = mid_date_str

    return mid_time


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 '
                  'Safari/537.36'
}

lst_r = []  # 内容数据
time_lst = []  # 时间
# 设置爬取长度，近一年（48周）
for i in tqdm(range(48)):
    # 265是当前周
    url = f'https://api.bilibili.com/x/web-interface/popular/series/one?number={265 - i}'
    # 存储数据集
    data = requests.get(url, headers=headers).json()['data']
    time_s = data['config']['name']  # 存储月份
    current_time = scrape_time(time_s)
    time_lst.append(current_time)

    lst_r.append(data['list'])
    time.sleep(random.uniform(1.5, 3))  # 休息片刻

# 爬取相关信息
time_video = [time_lst[i] for i, item in enumerate(lst_r) for name in item]  # 爬取时间
name_video = [name['title'] for item in lst_r for name in item]  # 爬取片名
owner = [name['owner']['name'] for item in lst_r for name in item]  # 爬取作者

# 部分媒体没有IP地址
pub_location = []
for i, item in enumerate(lst_r):
    for ip in item:
        try:
            pub_location.append(ip['pub_location'])
        except KeyError:
            pub_location.append(None)

rcmd_reason = [summary['rcmd_reason'] for item in lst_r for summary in item]  # 爬取摘要
url_video = [url['short_link_v2'] for item in lst_r for url in item]  # 爬取观看网址
view_num = [num['stat']['view'] for item in lst_r for num in item]  # 爬取观看次数
star_num = [num['stat']['like'] for item in lst_r for num in item]  # 爬取点赞数
holding_num = [num['stat']['favorite'] for item in lst_r for num in item]  # 爬取收藏数
coin_num = [num['stat']['coin'] for item in lst_r for num in item]  # 爬取投币数
share_num = [num['stat']['share'] for item in lst_r for num in item]  # 爬取转发数

# 创建字典，键是列名，值是数据列表
data = {
    '名称': name_video,
    'UP主': owner,
    'IP地址': pub_location,
    '视频摘要': rcmd_reason,
    '网站': url_video,
    '时间': time_video,
    '观看次数': view_num,
    '点赞数': star_num,
    '收藏数': holding_num,
    '投币数': coin_num,
    '转发数': share_num
}
# 创建一个数据框
df = pd.DataFrame(data)
# 将数据框写入CSV文件，并去除索引列
df.to_csv(r'b站每周必看（近一年）.csv', index=False, encoding='utf-8-sig')

print('运行完成！')
