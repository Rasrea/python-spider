import requests
import re
import pandas as pd
import numpy as np
import time
import random

from bs4 import BeautifulSoup
from tqdm import tqdm

# 设置虚拟代理
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}


# 从字符串中获取对应的键值
def string_to_value(string):
    try:
        _, value = string.strip().split(':', 1)
        item = [item.strip() for item in value.split('\n') if len(item.strip()) > 0]
        return ','.join(item)
    except ValueError:
        return np.nan


# 获取HTML中的详细数据
def scape_data(url, html):
    # 开始炖汤
    soup = BeautifulSoup(html, 'lxml')

    # 获取 MetaScore 和 UserScore
    score_pattern = re.compile(r'<span data-v-e408cafe>(.*?)</span>', re.S)
    scores = re.findall(score_pattern, html)
    meta_score = scores[0] if len(scores) > 0 else np.nan
    user_score = scores[1] if len(scores) > 1 else np.nan

    # 获取 Platforms
    platform_string = soup.find('div', attrs={'class': 'c-gameDetails_Platforms u-flexbox u-flexbox-row'})
    platform = string_to_value(platform_string.text) if platform_string else np.nan

    # 获取 Developer
    developer_string = soup.find('div', attrs={'class': 'c-gameDetails_Developer u-flexbox u-flexbox-row'})
    developer = string_to_value(developer_string.text) if developer_string else np.nan

    # 获取 Genres
    genres_string = soup.find('div', attrs={
        'class': 'c-gameDetails_sectionContainer u-flexbox u-flexbox-row u-flexbox-alignBaseline'})
    genres = string_to_value(genres_string.text) if genres_string else np.nan

    # 获取 Rated
    rated_pattern = re.compile(r'<span class="u-block">(.*?)</span>', re.S)
    match = re.search(rated_pattern, html)
    rated = match.group(1).strip() if match else np.nan

    # 整合数据
    game_detail = {
        'DetailUrl': url,  # 详细网址
        'MetaScore': meta_score,  # 综合评分
        'UserScore': user_score,  # 用户评分
        'Platforms': platform,  # 平台
        'Developer': developer,  # 开发商
        'Genres': genres,  # 标签类型
        'Rated': rated  # 游戏分级
    }
    return game_detail


# 获取网站HTML，每爬取50个网站存储一次 CSV
def scape_web(i, url_lst):
    data = []
    first_index = i + 1
    for url in tqdm(url_lst):
        try:
            html = requests.get(url, headers=headers).text
            element = scape_data(url, html)
            data.append(element)
            i += 1

            # 检查爬取个数，并存储文件
            if len(data) % 50 == 0:
                path = rf"D:\DESKTOP\gameData\t_data({first_index}-{i}).csv"
                t_df = pd.DataFrame(data)
                t_df.to_csv(path, index=False, encoding='utf-8-sig')

                # 每爬取50个网站，休息一会
                time.sleep(random.uniform(2, 3))
        except requests.exceptions.ProxyError:
            print(f'{i}.{url}')
            break

    return data


# 主函数
# 读取游戏详细网址
df = pd.read_csv(r"D:\Study\Python\DataVisualization\datasets\Metacritic\games(2003-2024).csv")

index = 5000

urls = df['DetailUrl'][index:]

# 获取游戏详细数据
game_data = scape_web(index, urls)

# 转为 DataFrame 并存储为 CSV
game_df = pd.DataFrame(game_data)
file_path = r'd:\desktop\detail_data.csv'
game_df.to_csv(file_path, index=False, encoding='utf-8-sig')
