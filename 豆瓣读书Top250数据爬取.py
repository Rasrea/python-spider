import requests
import re#稍微使用正则表达式
from bs4 import BeautifulSoup
import csv
#设置虚拟代理，模仿浏览器以避开反爬机制
headers={
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57'
}
#添加空列表以存储爬取内容
Photo = []
Score = []
People = []
t_price = []
Price = []
Publishment = []
Writer = []
Time = []
Name = []
for i in range(0,250,25):
    #利用requests库获取网页源代码
    r = requests.get(f"https://book.douban.com/top250?start={i}", headers = headers)
    bs = BeautifulSoup(r.text, 'html.parser')
    #利用BeautifulSoup库解析源代码
    #本次爬虫多次使用字符串切割
    #书名
    lst1 = bs.find_all('div', {'class':'pl2'})
    for t in lst1:
        Name.append(t.text.split()[0].strip())
    #时间
    lst2 = bs.find_all('p', {'class':'pl'})
    for t in lst2: 
        if '元' in t.text.split('/')[-2]:
            Time.append(t.text.split('/')[-3].strip())
        else:
            Time.append(t.text.split('/')[-2].strip())
    #作者
    lst3 = bs.find_all('p', {'class':'pl'})
    for t in lst3:
        Writer.append(t.text.split('/')[0])
    #出版社
    #考虑到某些出版社名字，因此使用了三次'in'
    lst4 = bs.find_all('p', {'class':'pl'})
    for t in lst4:
        for tt in t.text.split('/'):
            if '出版' in tt or '书店' in tt or '书局' in tt or '书馆' in tt:
                Publishment.append(tt)
    #评论人数
    lst6 = bs.find_all('span', {'class':'pl'})
    for t in lst6:
        if 'Top' in t.text.split()[1]:
            continue
        People.append(t.text.split()[1][:-3])
    #评分
    lst7 = bs.find_all('span', {'class':'rating_nums'})
    for t in lst7:
        Score.append(t.text)
    #封面
    #本段代码比较不稳定，可能是封面图片的地址不断更新，因此后续compile（）可能要改变
    lst8 = bs.find_all('img', {'src':re.compile('img')})
    for t in lst8:
        Photo.append(t['src'])
#价钱
    lst5 = bs.find_all('p', {'class':'pl'})
    for t in lst5:
        t_price.append(t.text.split('/')[-1].replace('元','').strip())
#这是Price的过滤代码，不得不说有些书是真的便宜
for tt in t_price:
    if 'N'in tt:
        Price.append(tt[3:].strip())
    else:
        Price.append(tt)
#为了便于数据分析，过滤时间列表去除月日
TTime = []
for t in Time:
    if '-' in t:
        TTime.append(t.split('-')[0])
    elif '年' in t:
        TTime.append(t.split('年')[0]) 
    elif '.' in t:
        TTime.append(t.split('.')[0])
    else:
        TTime.append(t)
#填写数据
with open(r"D:\Desktop\top250books.csv", 'w+', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['排名', '书籍','封面', '作者', '时间', '时间（无月日）', '出版社', '评分', '评价人数（人）', '售价（元）'])
    for i, (name, photo, _writer, time, ttime, publishment, score, people, price) in enumerate(zip(Name, Photo, Writer, Time, TTime, Publishment, Score, People, Price)):
        writer.writerow([i+1, name, photo, _writer, time, ttime,  publishment, score, people, price])
print('运行成功！')
