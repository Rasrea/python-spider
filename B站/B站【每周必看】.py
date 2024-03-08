import requests
import csv

url = 'https://api.bilibili.com/x/web-interface/popular/series/one?number=244'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 '
                  'Safari/537.36 Edg/119.0.0.0'
}
# 存储数据集
lst_r = requests.get(url, headers=headers).json()['data']['list']
# 定义保存地址
addr = input(r'请输入下载位置(如d:\desktop\data)：')

# 分类数据
Name = []  # 片名
Writer = []  # 作者
IP = []  # IP地址
Summary = []  # 摘要
Url = []  # 观看网址
View = []  # 观看次数
Like = []  # 点赞数
Collection = []  # 收藏数
Coin = []  # 投币数
Share = []  # 转发数

for data in lst_r:
    Name.append(data['title'])  # 爬取片名
    Writer.append(data['owner']['name'])  # 爬取作者
    IP.append(data['pub_location'])  # 爬取IP地址
    Summary.append(data['rcmd_reason'])  # 爬取摘要
    Url.append(data['short_link_v2'])  # 爬取观看网址
    View.append(data['stat']['view'])  # 爬取观看次数
    Like.append(data['stat']['like'])  # 爬取点赞数
    Collection.append(data['stat']['favorite'])  # 爬取收藏数
    Coin.append(data['stat']['coin'])  # 爬取投币数
    Share.append(data['stat']['share'])  # 爬取转发数

# 使用'w'创建一个csv文件并命名为f
path = addr + str('.csv')
with open(path, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(
        ['排名', '视频名', '作者', 'IP地址', '摘要', '观看网址', '观看次数', '点赞数', '收藏数', '投币数', '转发数'])
    for i, (name, _writer, ip, summary, url, view, like, collection, coin, share) in enumerate(
            zip(Name, Writer, IP, Summary, Url, View, Like, Collection, Coin, Share)):
        writer.writerow([i + 1, name, _writer, ip, summary, url, view, like, collection, coin, share])

print('运行完成！')
input("please input any key to exit!")
