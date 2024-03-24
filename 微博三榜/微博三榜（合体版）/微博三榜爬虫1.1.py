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
for key in url_lst:
    url = url_lst[key]

    # 获取相关榜单内容
    if j == 1:
        lst_r = requests.get(url, headers=headers).json()['data']['band_list']
    if j == 2:
        lst_r = requests.get(url, headers=headers).json()['data']['realtime']
    if j == 3:
        lst_r = requests.get(url, headers=headers).json()['data']['band_list']

    rank_lst = [int(i) for i in range(1, len(lst_r) + 1)]  # 生成排名

    if j == 3:
        note_topic = [item['topic'] for item in lst_r]  # 爬取（要闻）主题
        claim_where = [item['claim'].split('_')[1] for item in lst_r]  # 爬取（要闻）出处

        summary = ['无' if len(item['summary']) == 0 else
                   item['summary'] for item in lst_r]  # 爬取（要闻）简介
        people_read = [item['read'] for item in lst_r]  # （要闻）爬取阅读量
        mention = [item['mention'] for item in lst_r]  # （要闻）爬取讨论数

    else:
        note_topic = [item['note'] for item in lst_r]  # 爬取（文娱，热搜）词条
        # 需要检查‘hot_num’或‘raw_hot’是否存在
        hot = [item['hot_num'] if j == 1 else item['raw_hot'] if j == 2 else '-1'
               for item in lst_r if 'hot_num' in item or 'raw_hot' in item]  # 爬取热度, （热搜榜
        # 同理爬取“状态”，需要检查字典中是否有'icon_desc'
        state_text = [item['icon_desc'] if 'icon_desc' in item else '普通' for item in lst_r]

    type_text = [item['category'].split('|')[0] if j == 3 else item['category']
            if 'category' in item else '无' for item in lst_r]  # 爬取类型

    # 爬取网址（文娱，热搜，要闻）
    web = []
    for item in note_topic:
        t = 'https://s.weibo.com/weibo?q=' + str(item)
        web.append(t)

    # 将列表数据转换为DataFrame
    if j == 3:
        df = pd.DataFrame({
            '排名': rank_lst,
            '主题': note_topic,
            '出处': claim_where,
            '类型': type_text,
            '简介': summary,
            '阅读量': people_read,
            '讨论量': mention,
            '网址': web
        })
    else:
        df = pd.DataFrame({
            '排名': rank_lst,
            '词条': note_topic,
            '状态': state_text,
            '类型': type_text,
            '热度': hot,
            '网址': web
        })

    # 将DataFrame写入CSV文件，指定编码为UTF-8
    t_addr = f'微博({key}).csv'
    df.to_csv(t_addr, index=False, encoding='utf-8-sig')
    j = j + 1  # 迭代榜单
    print(f'({key})爬取完成！')
