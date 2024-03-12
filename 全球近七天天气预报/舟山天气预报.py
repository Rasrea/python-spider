# 数据来源：中国天气网
import requests
from bs4 import BeautifulSoup
import matplotlib
from matplotlib import pyplot as plt

# 设置字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 设置请求头，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 '
                  'Safari/537.36'
}


# 包含数据获取，解析与可视化
def main():
    url = 'http://www.weather.com.cn/weather/101211106.shtml'
    r = requests.get(url, headers=headers)  # 获取HTML
    # 数据清洗
    grouped_weather_lst = bath_data(r)

    # 收集数据，包括时间，天气，温度
    date_time = [item[0] for item in grouped_weather_lst]  # 时间
    weather_day = [item[1] for item in grouped_weather_lst]  # 天气
    temperature = [item[2] for item in grouped_weather_lst]  # 温度

    # 数据可视化
    line_picture(date_time, weather_day, temperature)  # 折线图


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


# 画折线图
def line_picture(date_time, weather_day, temperature):
    # 使用列表推导式进一步处理数据
    max_tem = [int(i.split('/')[0].replace('℃', '')) for i in temperature]  # 最高气温
    min_tem = [int(i.split('/')[1].replace('℃', '')) if len(i.split('/')) == 2
               else int(i.split('/')[0].replace('℃', '')) for i in temperature]  # 最低气温    # 竖排横坐标标签， 加空行符号
    day_lst = [date_time[i].replace('（', '\n（') +
               '\n' + weather_day[i] for i in range(len(date_time))]

    # 可视化数据
    fig = plt.figure(figsize=(12, 8))  # 创建图像对象
    plt.plot(range(len(day_lst)), max_tem, 's-', label='最高气温')  # 最高气温，并防止横坐标出现两个点
    plt.plot(range(len(day_lst)), min_tem, 'o--', label='最低气温')  # 最低气温，同理
    plt.xticks(range(len(day_lst)), day_lst)  # 设置横坐标标签
    plt.legend()  # 显示图例
    # 设置标签
    plt.title('舟山七日天气预报', fontsize=16)
    plt.xlabel('时间和天气', fontsize=14)
    plt.ylabel('温度（℃）', fontsize=14)

    fig.savefig('舟山七日天气预报.png')  # 保存图像
    plt.show()
    print('运行完成！')


# 开始运行
if __name__ == '__main__':
    main()
