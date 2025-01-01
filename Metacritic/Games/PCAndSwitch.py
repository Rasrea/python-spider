import requests
import re
import pandas as pd

from tqdm import tqdm

# 设置虚拟代理
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}


# 获取游戏数据
def scrape_data(html):
    # 获取游戏名称
    name_pattern = re.compile(r'<div data-title="(.*?)" class="c-finderProductCard_title"', re.S)
    games_name_lst.extend(re.findall(name_pattern, html))

    # 获取详细网址
    url_pattern = re.compile(r'<a href="(.*?)" class="c-finderProductCard_container g-color-gray80 u-grid">', re.S)
    detail_urls = re.findall(url_pattern, html)
    detail_urls[0] = re.findall(r'<a href="(/game/.*?/)', detail_urls[0])[-1]  # 纠正第一个网页、
    base_url = 'https://www.metacritic.com'
    detail_urls_lst.extend([base_url + url for url in detail_urls])

    # 获取游戏发布时间
    date_pattern = re.compile(r'<span class="u-text-uppercase">(.*?)</span>', re.S)
    games_date = re.findall(date_pattern, html)
    games_date_lst.extend([item.strip() for item in games_date])


# 获取网页HTML
def scrape_html(urls_lst):
    for url in tqdm(urls_lst):
        html = requests.get(url, headers=headers).text

        # 爬取详细数据
        scrape_data(html)


# 转为 DataFrame 类型，并保存为csv文件
def store_data(csv_path):
    df = pd.DataFrame({
        'Name': games_name_lst,
        'DetailUrl': detail_urls_lst,
        'ReleaseDate': games_date_lst
    })

    df.to_csv(csv_path, index=False, encoding='utf-8-sig')


# 主函数
games_name_lst = []  # 存储游戏名称
detail_urls_lst = []  # 存储详细页面
games_date_lst = []  # 存储游戏发布时间

# 获取数据
base = 'https://www.metacritic.com/browse/game/?releaseYearMin=2003&releaseYearMax=2024&platform=pc&platform=nintendo-switch&page='
urls = [base + str(i) for i in range(1, 2)]
scrape_html(urls)

# 存储数据
# file_path = r'd:\desktop\data5.csv'
# store_data(file_path)

print(detail_urls_lst)
