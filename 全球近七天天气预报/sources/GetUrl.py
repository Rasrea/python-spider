from ScrapeData import scrape_data
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import re


def get_url():
    # 配置浏览器，并打开网站
    driver = webdriver.Chrome()
    driver.get('http://www.weather.com.cn/')
    # 等待网页加载
    time.sleep(2)

    # 寻找搜索框位置
    input_box = driver.find_element(By.XPATH, "//input[@type='text']")

    # 自定义地址
    my_site = input('请输入地点：')
    input_box.send_keys(my_site)
    input_box.click()
    time.sleep(1)
    html = driver.page_source  # 保存网站源代码

    # 关闭浏览器
    driver.quit()

    # 获取7天数据所对应的网址
    result = re.search('<li.*?num="(.*?)">', str(html)).group(1)
    url = f'http://www.weather.com.cn/weather/{result}.shtml'

    scrape_data(url, my_site)  # 处理数据
