import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 "
                  "Safari/537.36"
}

xhr_url = ('https://piaofang.maoyan.com/dashboard-ajax/movie?orderType=0&uuid=e6d8b57f-239f-494e-a887-30f99b6644bf'
           '&timeStamp=1708759023024&User-Agent'
           '=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMi4wLjAuMCBTYWZhcmkvNTM3LjM2&index=67&channelId=40009&sVersion=2&signKey=12e8631f7734a89bfb700cd64ea8bf11')
xhr_data = requests.get(xhr_url, headers=headers).json()
movie_list = xhr_data['movieList']['list']

# 爬取其他信息
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

print(avg_seat)
print(len(avg_seat))