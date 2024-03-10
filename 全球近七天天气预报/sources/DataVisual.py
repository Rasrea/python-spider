from matplotlib import pyplot as plt
import os

# 配置环境
plt.style.use('seaborn-v0_8')  # 使用seaborn风格
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


# 画折线图
def line_picture(date_time, weather_day, temperature, my_site):
    # 使用列表推导式进一步处理数据
    max_tem = [int(i.split('/')[0].replace('℃', '')) for i in temperature]  # 最高气温
    min_tem = [int(i.split('/')[1].replace('℃', '')) if len(i.split('/')) == 2
               else int(i.split('/')[0].replace('℃', '')) for i in temperature]  # 最低气温，解决最低与最高温相同的问题
    # 竖排横坐标标签——加空行符号
    day_lst = [date_time[i].replace('日', '日\n') +
               '\n' + weather_day[i] for i in range(len(date_time))]

    # 可视化数据
    fig = plt.figure(figsize=(12, 8))  # 创建图形对象
    plt.plot(range(len(day_lst)), max_tem, 's-', label='最高气温')  # 最高气温，并防止横坐标出现两个点
    plt.plot(range(len(day_lst)), min_tem, 'o-', label='最低气温')  # 最低气温，同理
    plt.xticks(range(len(day_lst)), day_lst)  # 设置横坐标标签
    plt.legend()  # 显示图例
    # 设置标签
    plt.title(f'{my_site}七日天气预报', fontsize=16)
    plt.xlabel('时间和天气', fontsize=14)
    plt.ylabel('温度（℃）', fontsize=14)
    plt.grid(True)  # 添加网格

    # 定义文件保存地址
    t_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 绝对地址
    file_path = os.path.join(t_path, '数据集')
    os.makedirs(file_path, exist_ok=True)  # 创建文件路径（如果不存在）
    pic_path = os.path.join(file_path, f'{my_site}七日天气预报.png')

    fig.savefig(pic_path)  # 保存图像
    plt.show()
    print(f'图片保存在：{pic_path}')  # 打印图片地址
    print('运行完成！')
