import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
# 读取数据集
df = pd.read_csv("D:\Desktop\douban.csv")
# 设置字体、风格等
sns.set(font='SimHei', style='whitegrid')
# 绘制电影评分的分布曲线和直方图，图1
#分值总要集中在8.5-9.5之间
sns.histplot(df['评分'], kde=True, bins=40)
plt.title('电影评分汇总')
plt.xlabel('评分')
plt.ylabel('数量')
plt.show()
#绘制电影时间的分布曲线和直方图，图2
sns.histplot(df['时间'], kde=True, bins=100)
plt.title('电影时间汇总')
plt.xlabel('时间')
plt.ylabel('数量')
plt.show()
# 绘制电影评分和时间的关系图，图3
#电影越老越经典，评分越高
sns.scatterplot(x='评分', y='时间', data=df)
sns.regplot(x='评分', y='时间', data=df, scatter=False, color='red')
plt.title('电影评分和时间的关系图')
plt.xlabel('评分')
plt.ylabel('时间')
plt.show()
# 绘制电影时间和评论人数的关系图，图4
#随着多媒体时代的到来，1980年以后评论人数猛增
sns.scatterplot(x='时间', y='评价人数(人)', data=df)
sns.regplot(x='时间', y='评价人数(人)', data=df, scatter=False, color='red')
plt.title('电影时间和评论人数的关系图')
plt.xlabel('时间')
plt.ylabel('人数')
plt.show()
# 绘制电影评分和评论人数的关系图，图5
#群众的眼睛是雪亮，高分都是经过众人的一致认可
sns.scatterplot(x='评分', y='评价人数(人)', data=df)
sns.regplot(x='评分', y='评价人数(人)', data=df, scatter=False, color='red')
plt.title('电影评分和评论人数的关系图')
plt.xlabel('评分')
plt.ylabel('人数')
plt.show()
# 计算各个国家和地区电影数量并绘制前十名的饼图，图6
top_countries = df['国家'].value_counts().head(10)
plt.figure(figsize=(8,8))
plt.pie(top_countries, labels=top_countries.index, labeldistance=1.1, autopct='%1.1f%%')
plt.title('豆瓣 Top 250 各个国家和地区电影数量占比')
plt.show()
# 计算每个导演电影数量并绘制前十名的饼图，图7
top_countries = df['导演'].value_counts().head(10)
plt.figure(figsize=(8,8))
plt.pie(top_countries, labels=top_countries.index, labeldistance=1.1, autopct='%1.1f%%')
plt.title('豆瓣 Top 250 每个导演电影数量占比')
plt.show()
#计算每个电影类型数量并绘制前十名的饼图,图8
top_countries = df['类型'].value_counts().head(10)
plt.figure(figsize=(8,8))
plt.pie(top_countries, labels=top_countries.index, labeldistance=1.1, autopct='%1.1f%%')
plt.title('豆瓣 Top 250 电影类型占比')
plt.show()
