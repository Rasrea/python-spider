from DataVisual import line_picture
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 '
                  'Safari/537.36'
}


def scrape_down(data_url, my_site):
    # 创建 Chrome 浏览器选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 启用无头模式
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(data_url)

    # 等待网页加载
    time.sleep(2)
    html = driver.page_source  # 保存此时的网站源代码

    # 爬取温度（最高和最低）
    result = re.findall(r'<tspan.*?>(.*?)</tspan>', html, re.S)
    max_tem = [int(i.replace('°C', '')) for i in result[:8]]
    min_tem = [int(j.replace('°C', '')) for j in result[8:16]]

    # 日期
    result2 = re.findall(r'<p class="date">(.*?)</p>.*?class="date-info">(.*?)</p>',
                         html, re.S)
    date_time = [t[0] + '\n' + '(' + t[1] + ')' for t in result2]  # 加空行符号，便于画图

    # 天气， 并组合日期和天气
    result3 = re.findall(r'<p class="weather-info.*?>(.*?)</p>', str(html), re.S)
    weather_day = [i.strip() for i in result3]
    date_weather = [date_time[i] + '\n' + weather_day[i] for i in range(len(date_time))]

    line_picture(max_tem, min_tem, date_weather, my_site)  # 可视化分析


if __name__ == '__main__':
    url = 'https://forecast.weather.com.cn/town/weathern/101181407002.shtml'
    scrape_down(url)
