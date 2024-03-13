from ScrapeCity import scrape_city  # 爬取城市信息
from ScrapeDown import scrape_down  # 爬取乡镇信息
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
    my_site = input('请输入城市名称：')
    input_box.send_keys(my_site)  # 输入搜索框
    input_box.click()  # 点击搜索框，让网站显示“搜索建议”
    time.sleep(1)
    html = driver.page_source  # 保存此时的网站源代码

    # 关闭浏览器
    driver.quit()

    # 组合成该地点7天数据所对应的网址
    result = re.findall('<li.*?num="(.*?)">', str(html))  # 获取对应标签
    # 收集相关地方
    site_lst = []
    for i in result:
        site = re.search(f'num="{i}">(.*?)</li>', str(html), re.S)  # 有待改进html
        site_lst.append(site.group(1).replace('<b>', '').replace('</b>', ''))
    # 选择详细地址
    for j, item in enumerate(site_lst):
        print(f'{j + 1}. {item}')
    home_site = eval(input('选择详细地址（序号）：'))
    if len(result[home_site - 1]) == 9:
        url = f'http://www.weather.com.cn/weather/{result[home_site - 1]}.shtml'
        scrape_city(url, site_lst[home_site - 1])  # 爬取城市信息
    else:
        url = f'https://forecast.weather.com.cn/town/weathern/{result[home_site - 1]}.shtml'
        scrape_down(url, site_lst[home_site - 1])
