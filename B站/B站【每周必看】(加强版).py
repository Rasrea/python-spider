import requests
import re
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import json
import pickle


class BilibiliWeekly:
    def __init__(self, current_week=276, range_time=48, csv_file='b站每周必看（近一年）.csv', cookies_file=None):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/129.0.0.0 Safari/537.36'
        }
        self.session = requests.Session()
        self.lst_r = []  # 内容数据
        self.range_time = range_time  # 时间范围（周）
        self.time_lst = []  # 存储时间
        self.current_week = current_week  # 当前周
        self.csv_path = csv_file  # 保存地址
        self.cookies_file = cookies_file
        self.load_cookies()  # 加载cookies

    def load_cookies(self):
        # 加载cookies并设置到session中
        if self.cookies_file:
            with open(self.cookies_file, "rb") as file:
                cookies = pickle.load(file)
            for cookie in cookies:
                self.session.cookies.set(cookie['name'], cookie['value'])

    @staticmethod
    def scrape_time(s):
        match = re.search(r'(.*?)第(.*?)期(.*?-.*$)', s)
        if not match:
            return None
        time_str = match.group(3).strip().replace(' ', '')
        start_date_str, end_date_str = time_str.split('-')
        year = match.group(1)
        start_date_str = year + '.' + start_date_str
        end_date_str = year + '.' + end_date_str

        try:
            start_date = datetime.strptime(start_date_str, '%Y.%m.%d')
            end_date = datetime.strptime(end_date_str, '%Y.%m.%d')
        except ValueError as e:
            print(f"日期转换错误: {e}")
            return None

        mid_date = start_date + (end_date - start_date) / 2
        return mid_date.strftime('%Y-%m-%d')

    def store_to_csv(self, data):
        df = pd.DataFrame(data)
        df.to_csv(self.csv_path, index=False, encoding='utf-8-sig')

    def screen_data(self):
        return {
            '名称': [name['title'] for item in self.lst_r for name in item],
            'UP主': [name['owner']['name'] for item in self.lst_r for name in item],
            'IP地址': [ip.get('pub_location', None) for item in self.lst_r for ip in item],
            '热评': [summary['rcmd_reason'] for item in self.lst_r for summary in item],
            '网站': [url['short_link_v2'] for item in self.lst_r for url in item],
            '时间': [self.time_lst[i] for i, item in enumerate(self.lst_r) for _ in item],
            '观看次数': [num['stat']['view'] for item in self.lst_r for num in item],
            '点赞数': [num['stat']['like'] for item in self.lst_r for num in item],
            '收藏数': [num['stat']['favorite'] for item in self.lst_r for num in item],
            '投币数': [num['stat']['coin'] for item in self.lst_r for num in item],
            '转发数': [num['stat']['share'] for item in self.lst_r for num in item],
        }

    def get_json(self, url):
        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None

    def scrape_web(self):
        for i in tqdm(range(self.range_time)):
            url = f'https://api.bilibili.com/x/web-interface/popular/series/one?number={self.current_week - i}'
            json_data = self.get_json(url)
            if json_data and 'data' in json_data:
                data = json_data['data']
                self.lst_r.append(data['list'])
                current_time = self.scrape_time(data['config']['name'])
                self.time_lst.append(current_time if current_time else '未知')
            else:
                print('数据为空或解析失败')
                continue

        data = self.screen_data()
        self.store_to_csv(data)
        print('数据抓取完成！')


# 定义实例
if __name__ == '__main__':
    file_path = r'd:\desktop\newbili.csv'
    range_time = 5  # 时间范围（周）
    current_week = 301  # 当前期号，倒叙
    cookies_file = r"D:\Study\Python\Spiders\模拟登录\cookies\bilibili_nyj.pkl"

    # 创建实例
    bilibili_spider = BilibiliWeekly(current_week=current_week,
                                     range_time=range_time,
                                     csv_file=file_path,
                                     cookies_file=cookies_file)
    bilibili_spider.scrape_web()
