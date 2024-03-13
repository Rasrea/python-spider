from matplotlib import pyplot as plt
import os

# 配置环境
plt.style.use('seaborn-v0_8')  # 使用seaborn风格
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


# 画折线图
def line_picture(max_tem, min_tem, date_weather, my_site):
    # 可视化数据
    fig = plt.figure(figsize=(14, 10))  # 创建图形对象
    plt.plot(range(len(date_weather)), max_tem, 's-', label='最高气温')  # 最高气温，并防止横坐标出现两个点
    plt.plot(range(len(date_weather)), min_tem, 'o-', label='最低气温')  # 最低气温，同理
    plt.xticks(range(len(date_weather)), date_weather)  # 设置横坐标标签
    plt.legend()  # 显示图例
    # 设置标签
    plt.title(f'{my_site} 七日天气预报', fontsize=16)
    plt.xlabel('时间和天气', fontsize=14)
    plt.ylabel('温度（℃）', fontsize=14)

    # 定义文件保存地址
    t_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 绝对地址
    file_path = os.path.join(t_path, '数据集')
    os.makedirs(file_path, exist_ok=True)  # 创建文件路径（如果不存在）
    pic_path = os.path.join(file_path, f'{my_site}七日天气预报.png')

    fig.savefig(pic_path)  # 保存图像
    plt.show()

    print('\n')
    print(f'图片保存在：{pic_path}')  # 打印图片地址
    print('运行完成！')
