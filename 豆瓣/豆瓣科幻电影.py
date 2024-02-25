import requests
import time
import random
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 '
                  'Safari/537.36 Edg/121.0.0.0'
}

# 定义空列表，存储数据
film_name = []  # 名称
cover_url = []  # 封面
detail_url = []  # 详情页面
film_type = []  # 类型
film_regions = []  # 国家
vote_count = []  # 评价人数
release_time = []  # 上映时间
score = []  # 评分
actors = []  # 演员
actor_count = []  # 演员个数

total_progress = 200  # 设置进度条


# 保存数据
def store_data(lst_data):
    # 为了方便导入，转置数据并加入排名
    transposed_data = [[i + 1] + list(row) for i, row in enumerate(zip(*lst_data))]
    # 自定义列名
    columns = ['排名', '名称', '封面', '详细内容', '类型', '国家',
               '上映时间', '评价人数', '评分', '演员数', '演员']

    # 将DataFrame写入CSV文件
    df = pd.DataFrame(transposed_data, columns=columns)
    csv_file = 'd:\desktop\data.csv'
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')

    print('\n爬取完成!')


# 爬取数据包括：名称，封面，详细内容，类型...
def scrape_data(lst_r):
    # 检索数据
    for data in lst_r:
        film_name.append(data['title'])  # 保存名称
        cover_url.append(data['cover_url'])  # 保存封面网址
        detail_url.append(data['url'])  # 保存详情页面
        film_type.append(data['types'])  # 保存类型
        film_regions.append(data['regions'])  # 保存国家
        vote_count.append(data['vote_count'])  # 保存评价人数
        release_time.append(data['release_date'])  # 保存上映时间
        score.append(data['score'])  # 保存评分
        actors.append(data['actors'])  # 保存演员
        actor_count.append(data['actor_count'])  # 保存演员个数


# 获取网址json数据
def make_url(base_url):
    try:
        lst_r = requests.get(base_url, headers=headers).json()  # 返回一个容量为20的列表
        scrape_data(lst_r)  # 爬取并存储数据
    except Exception as e:
        print(f"Error: {e}")


# 主函数
def main():
    for gap in range(0, total_progress + 1, 20):
        base_url = (f'https://movie.douban.com/j/chart/top_list?type=17&interval_id=100%3'
                    f'A90&action=&start={gap}&limit=20')
        make_url(base_url)  # 获取网址json数据
        time.sleep(random.uniform(1.0, 2.5))  # 随机化请求间隔时间
        # 计算进度条的长度
        progress_length = int(gap / total_progress * 50)
        progress_bar = '[' + '=' * progress_length + ' ' * (50 - progress_length) + ']'
        print(f'Progress: {gap}/{total_progress} {progress_bar}', end='\r', flush=True)

    # 合并数据
    lst_data = [film_name, cover_url, detail_url, film_type, film_regions,
                release_time, vote_count, score, actor_count, actors]
    # 将数据保存到文件中
    store_data(lst_data)


if __name__ == '__main__':
    main()

input('Please any keys to exit')