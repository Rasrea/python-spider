# python-spider
包含猫眼电影、天气预报、豆瓣Top读书和电影、b站、微博等。爬取信息都会保存在对应的csv文件中，其中数据可视化代码不具有通用性。 <br>

## 猫眼电影 <br>
### 基本功能：破译实时票房（综合和分账）并爬取其他简单数据。运行source文件中的main.py就会生成相应csv文件，并进行可视化，存储在同目录的数据集文件夹中。 <br>
增加图片识别模型，可以识别出画出的数字（原方法是强行找规律）  <br>
详细讲解请参考CSDN文章：https://blog.csdn.net/m0_74048576/article/details/136279937 <br>

## 全球天气预报（近七天） <br>
### 基本功能：爬取天气网中的数据，并进行可视化分析。运行sources文件中的begin.py，输入城市名称（中文）就会生成对应的图像。改进版将地点精确到乡镇 <br>
详细讲解请参考CSDN文章：https://blog.csdn.net/m0_74048576/article/details/136590761 <br>

## 豆瓣 <br>
### 基本功能：使用Beautiful Soup爬取豆瓣Top250读书、电影及科幻电影的相关信息，还有使用正则的例子。 <br>
--修复“科幻电影爬虫”的进度条在pycharm中无法显示的问题。增加豆瓣可视化代码  <br>

## B站 <br>
### 基本功能：爬取每周必看排行榜信息，由于网页使用动态渲染，因此采用api结合进行爬取。 <br>

## 微博三榜 <br>
### 基本功能：同时爬取微博热搜榜、文娱榜、要闻榜的相关信息。 <br>
--优化代码  <br>

仅供学习参考，不做商业用途
