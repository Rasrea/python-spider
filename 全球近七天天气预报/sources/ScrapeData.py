from DataVisual import line_picture
import requests
from bs4 import BeautifulSoup

# 设置请求头，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 '
                  'Safari/537.36'
}


# 包含数据获取，解析与可视化
def scrape_data(url, my_site):
    r = requests.get(url, headers=headers)  # 获取HTML
    # 数据清洗
    grouped_weather_lst = bath_data(r)

    # 收集数据，包括时间，天气，温度
    date_time = [item[0] for item in grouped_weather_lst]  # 时间
    weather_day = [item[1] for item in grouped_weather_lst]  # 天气
    temperature = [item[2] for item in grouped_weather_lst]  # 温度

    # 数据可视化
    line_picture(date_time, weather_day, temperature, my_site)  # 折线图


# 清洗数据
def bath_data(r):
    # 先用.content获取原始字节内容，防止出现乱码
    page_content = r.content
    bs = BeautifulSoup(page_content, 'html.parser')  # 设置解析器
    text_r = bs.find('ul', {'class': 't clearfix'})  # 找到天气数据
    t_weather = text_r.text.split('\n')  # 转换字符集
    weather_lst = [i for i in t_weather if len(i) != 0]  # 去除空格
    grouped_weather_lst = [weather_lst[n:n + 4] for n in range(0, len(weather_lst), 4)]  # 要求每四个组成一个子列表
    return grouped_weather_lst

