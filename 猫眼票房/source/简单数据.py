from 保存数据 import keep_data
import re


# 爬取简单信息
def simple_data(movie_list, combine_money, part_money, love_day):

    film_name = []  # 名称
    release_time = []  # 上映天数

    for lantern in movie_list:
        # 爬取上映天数
        t_time = lantern['movieInfo']['releaseInfo']
        if '天' in t_time:
            times = re.search('上映(.*?)天', t_time).group(1)
            release_time.append(times)  # 分离上映天数
        elif len(t_time) == 0:
            release_time.append('重映')  # 上映时间为空
        else:
            release_time.append(t_time)

        film_name.append(lantern['movieInfo']['movieName'])  # 爬取名称

    keep_data(combine_money, part_money, film_name, release_time, love_day)  # 导入csv文件
