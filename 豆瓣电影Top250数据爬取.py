import requests
from bs4 import BeautifulSoup
import csv
#设置虚拟代理，模仿浏览器以避开反爬机制
headers={
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57'
}
#添加空列表以存储爬取内容
Name=[]
Director=[]
Actor=[]
Time=[]
Country=[]
Type=[]
Score=[]
Person=[]
Comment=[]
t_Comment=[]#评语爬取较为麻烦，故创立一个转换列表
#使用for循环遍历top250
for i in range(0,250,25):
    #利用requests库获取网页源代码
    response=requests.get(f"https://movie.douban.com/top250?start={i}",headers=headers)
    html=response.text
    #利用BeautifulSoup库解析源代码
    soup=BeautifulSoup(html,"html.parser")
    all_names=soup.findAll("span",attrs={"class":"title"})
    for name in all_names:
        t=name.text
        if "/" not in t:
            Name.append(t)
    all_directors=soup.findAll("div", attrs={"class":"info"})
    #由于某些电影的导演不止一个，故切割字符串时会比较麻烦
    for item in all_directors:
        Director.append(item.text.split('导演')[1].split('\n')[0].split('   主')[0].strip().split(':')[1].strip()) 
    all_actors=soup.findAll("div", attrs={"class":"info"})
    for item in all_actors:
        Actor.append(item.text.split('主演:')[-1].split()[0])
    all_time=soup.findAll("div", attrs={"class":"info"})
    for item in all_time:
        #由于有些国产电影时间会有特殊标记（如（中国大陆）），故这里只取前四个字符
        Time.append(item.text.split('主演：')[0].split('/')[-3].strip().split('\n')[-1].strip()[:4])    
    all_countries=soup.findAll("div", attrs={"class":"info"})
    for item in all_countries:
        Country.append(item.text.split('主演：')[0].split('/')[-2].strip())
    all_types=soup.findAll("div", attrs={"class":"info"})
    for item in all_types:
        Type.append(item.text.split('主演:')[-1].split('/')[-1].strip().split('\n')[0])
    all_scores=soup.findAll("div",attrs={"class":"star"})
    for item in all_scores:
        Score.append(item.text.split('\n')[2])
    all_persons=soup.findAll("div",attrs={"class":"star"})
    for item in all_persons:
        Person.append(item.text.split('\n')[4][:-3])
    #由于某些电影没有影评，使用soup.findAll("span",attrs={"class":"inq"})不利于后期创建csv表格
    #使用此方法会爬取电影影评，若没有，则爬取电影的评论人数以充当影评
    all_comments=soup.findAll("div",attrs={"class":"info"})
    for item in all_comments:
        t_Comment.append(item.text.split('\n')[-4])
#遍历爬取的影评，利用 in 将以评论人数为影评的电影替换影评为：“无”
for item in t_Comment:
    if "人评价" in item:
        item="无"
        Comment.append(item)
        continue
    Comment.append(item)
#使用'w'创建一个csv文件并命名为f
with open(r"D:\Desktop\top250films.csv", 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['电影', '导演', '主演', '时间', '国家', '类型', '评分', '评价人数（人）', '评语'])
    for i, (name, director, actor, time, country, type_, score, person, comment) in enumerate(zip(Name, Director, Actor, Time, Country, Type, Score, Person, Comment)):
        writer.writerow([f'{i + 1}.{name}', director, actor, time, country, type_, score, person, comment])
print('运行完成')
