import pandas as pd
import matplotlib
from matplotlib import pyplot as plt

# 设置字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


# 存储文件信息，并进行可视化
def explain_data(csv_file_path, love_day):
    # 读取csv文件
    df = pd.read_csv(csv_file_path)
    columns = df.columns

    # 存储csv文件中的信息，并修改为相应的数据类型
    all_money = [float(i) for i in df[columns[2]] if float(i) > 0]  # 综合票房
    part_money = [df[columns[3]][i] for i in range(len(all_money))]  # 分账票房

    # 处理电影名，给每一个字符后加空行，长度超过5加省略号，实现文字竖排
    name_lst = []
    for i in range(len(all_money)):
        if len(df[columns[1]][i]) > 5:
            t = ''  # 中介字符串
            for j in df[columns[1]][i][:5].strip():
                t = t + j + '\n'
            t = t + '.' + '\n' + '.' + '\n' + '.'
            name_lst.append(t)
        else:
            tt = ''
            for jj in df[columns[1]][i]:
                tt = tt + jj + '\n'
            name_lst.append(tt)

    # 数据可视化，画折线图
    fig = plt.figure(figsize=(14, 12))  # 创建图像对象
    plt.plot(range(len(name_lst)), all_money, 's-', label='综合或预售')  # 综合票房，并防止横坐标出现两个点
    plt.plot(range(len(name_lst)), part_money, 'o--', label='分账或预售')  # 同理，分账票房
    plt.xticks(range(len(name_lst)), name_lst)  # 设置横坐标标签，并旋转90度
    plt.legend()  # 显示图例

    # 设置图形标签
    plt.title(f'猫眼电影{love_day}票房')
    plt.ylabel('万元')
    plt.grid(True)  # 添加网格
    fig.savefig(f'{csv_file_path}.png')  # 保存图像
    plt.show()

    print('程序处理完成！')
