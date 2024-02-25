import requests
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 '
                  'Safari/537.36 Edg/120.0.0.0',
    'Cookie': 'SUB=_2AkMSKJlSf8NxqwFRmfoXy2jka41zzgHEieKkdGiJJRMxHRl-yT9vqlU5tRB6Oai3vlM-tNtuokqqydEe_qjOt3Hd78HB; '
              'SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WW2FbZDRBZAlus.3VZVylxc; '
              'SINAGLOBAL=1593182467560.3235.1702106731121; XSRF-TOKEN=3IZY79X3XJnODFFA0aLIvFDl; '
              'WBPSESS=V0zdZ7jH8_6F0CA8c_ussX7v09Fe0lbDA-4S4-hZWYaHjife81Zh1U4ShoquMcDESVCJ6-exMCjCRMlbY2NOecLSo'
              '--AoT_osGI26YnnzrhVlffs3QdTFSt6RzFhGijjk8CtLJ_PWcaD2IRO1XSpicfQTK2ki0tHm5AJRNjPhwU=; '
              '_s_tentry=weibo.com; Apache=6502686030357.5625.1703596053330; '
              'ULV=1703596053358:3:3:2:6502686030357.5625.1703596053330:1703514491831; PC_TOKEN=1cc8d43f83; '
              'login_sid_t=1a3f5d027c7e947acea83759b8a0a3ff; cross_origin_proto=SSL; UOR=,,cn.bing.com'
}

url_lst = {
    '文娱榜': 'https://weibo.com/ajax/statuses/entertainment',
    '热搜榜': 'https://weibo.com/ajax/side/hotSearch',
    '要闻榜': 'https://weibo.com/ajax/statuses/news'
}

j = 1  # 计数器，用来区分三个网址
addr = input('请输入文件下载位置(d:\desktop\)：')  # 地址
for key in url_lst:
    url = url_lst[key]
    # 输入保存地址
    t_addr = addr + f'微博({key}).csv'
    if j == 1:
        lst_r = requests.get(url, headers=headers).json()['data']['band_list']
    if j == 2:
        lst_r = requests.get(url, headers=headers).json()['data']['realtime']
    if j == 3:
        lst_r = requests.get(url, headers=headers).json()['data']['band_list']

    i = 1
    Rank = []  # 排名

    # 要闻
    Note = []  # 词条（文娱，热搜），（要闻）的主题

    if j == 3:
        Claim = []  # （要闻）出处

        Summary = []  # （要闻）简介

        Read = []  # （要闻）阅读量

        Mention = []  # （要闻）讨论数

    else:
        State = []  # 状态（文娱，热搜）

        Hot = []  # 热度, 热搜与文娱不一致

    Type = []  # 类型（文娱，热搜，要闻）

    Web = []  # 网址（文娱，热搜）
    for item in lst_r:
        Rank.append(str(i))
        i = i + 1  # 爬取排名

        if j == 3:
            Note.append(item['topic'])  # 爬取（要闻）主题

            Claim.append(item['claim'].split('_')[1])  # 爬取（要闻）出处

            if len(item['summary']) == 0:  # 爬取（要闻）简介
                Summary.append('无')
            else:
                Summary.append(item['summary'])

            Read.append(item['read'])  # （要闻）爬取阅读量

            Mention.append(item['mention'])  # （要闻）爬取讨论数


        else:
            Note.append(item['note'])  # 爬取（文娱，热搜）词条
            try:
                if j == 1:
                    Hot.append(item['hot_num'])  # 爬取热度, （文娱榜）
                if j == 2:
                    Hot.append(item['raw_hot'])  # 爬取热度, （热搜榜）
            except KeyError:
                Hot.append('-1')

            try:
                State.append(item['icon_desc'])  # 爬取状态
            except KeyError:
                State.append('普通')  # 某些字典中没有'icon_desc'

        try:
            if j == 3:
                Type.append(item['category'].split('|')[0])  # 爬取（要闻）类型
            else:
                Type.append(item['category'])  # （文娱，热搜）爬取类型
        except KeyError:
            Type.append('无')

    # 爬取网址（文娱，热搜，要闻）
    for item in Note:
        t = 'https://s.weibo.com/weibo?q=' + str(item)
        Web.append(t)

    # 导入指定的csv文件中
    # 将列表数据转换为DataFrame
    if j == 3:
        df = pd.DataFrame({
            '排名': Rank,
            '主题': Note,
            '出处': Claim,
            '类型': Type,
            '简介': Summary,
            '阅读量': Read,
            '讨论量': Mention,
            '网址': Web
        })
    else:
        df = pd.DataFrame({
            '排名': Rank,
            '词条': Note,
            '状态': State,
            '类型': Type,
            '热度': Hot,
            '网址': Web
        })

    # 将DataFrame写入CSV文件，指定编码为UTF-8
    df.to_csv(t_addr, index=False, encoding='utf-8-sig')
    j = j + 1
    print(f'({key})爬取完成！')

input('Please enter any keys to exit!')
