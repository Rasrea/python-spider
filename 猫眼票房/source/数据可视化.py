import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

# 配置环境
plt.style.use('seaborn-v0_8')  # 使用seaborn风格
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


# 存储文件信息，并进行可视化
def explain_data(csv_file_path, love_day):
    # 读取csv文件
    df = pd.read_csv(csv_file_path)
    columns = df.columns
    sum_money = [float(i) for i in df[columns[2]]]  # 统计总票房

    # 存储csv文件中的信息，并修改为相应的数据类型
    part_money = [df[columns[3]][i] for i in range(15)]  # 分账票房，前15
    all_money = [df[columns[2]][i] for i in range(15)]  # 综合票房

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

    # 数据可视化，画折线图，前15名
    fig = plt.figure(figsize=(14, 12))  # 创建图像对象
    plt.plot(range(len(name_lst)), all_money, 's-', label='综合或预售')  # 综合票房，并防止横坐标出现两个点
    plt.plot(range(len(name_lst)), part_money, 'o--', label='分账或预售')  # 同理，分账票房
    plt.xticks(range(len(name_lst)), name_lst)  # 设置横坐标标签
    plt.legend()  # 显示图例

    # 设置图形标签
    plt.title(f'猫眼电影{love_day}票房（前十五）', fontsize=14)
    plt.ylabel('万元', fontsize=14)
    pic_path1 = csv_file_path.replace('.csv', '折线图')  # 调整图片地址
    fig.savefig(f'{pic_path1}.png')  # 保存图像

    # 只显示name_lst的前四个，剩余的组成一组
    top_names = list(df[columns[1]])[:4] + ['其他'] # 标签
    other_total = sum(all_money[4:])
    # 合并剩余的数据为一个“其他”类别
    top_money = all_money[:4] + [other_total]

    '''# 绘制饼图
    fig = plt.figure(figsize=(12, 8))  # 创建图像对象
    explode = [0, 0, 0, 0, 0.1]  # 爆炸第五个扇形（’其他‘）

    # 绘制并突出最大的扇形部分
    plt.pie(top_money, explode=explode, autopct='%1.1f%%', shadow=True, startangle=140, textprops={'fontsize': 14})
    plt.title(f'{love_day}四天王（总{round(sum(sum_money), 1)}万）', fontsize=18)  # 显示总票房，保留一位小数
    plt.legend(top_names, loc="best")  # 绘制图例，loc寻找最佳位置
    plt.axis('equal')  # 确保饼图是圆形，而不是椭圆形
    pic_path2 = csv_file_path.replace('.csv', '饼图')  # 调整图片地址
    fig.savefig(f'{pic_path2}.png')  # 保存图像'''

    # 创建环形图
    fig1, ax1 = plt.subplots(figsize=(13, 8))
    wedges, texts, autotexts = ax1.pie(top_money, startangle=90, pctdistance=0.85, autopct='%1.1f%%')

    # 调整标签和自动注释的字体大小
    for text in texts + autotexts:
        text.set_fontsize(14)

    # 绘制一个白色的圆在中心（将饼图转换为环形图）
    centre_circle = plt.Circle((0, 0), 0.60, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # 添加注释
    # 注释样式，arrowprops：箭头样式，bbox：文本框的样式，zorder：注释的层级，va：注释的对齐方式
    kw = dict(arrowprops=dict(arrowstyle='-'), zorder=0, va='center')

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1) / 2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: 'right', 1: 'left'}[int(np.sign(x))]
        connection_style = 'angle,angleA=0,angleB={}'.format(ang)
        kw['arrowprops'].update({'connectionstyle': connection_style})

        # 完善名称格式，防止过长
        if '：' in top_names[i]:
            name_parts = top_names[i].split('：')
            # 使用ljust添加空格并左对齐
            formatted_name = name_parts[0] + '：\n' + name_parts[1].ljust(10)
            top_names[i] = formatted_name

        ax1.annotate(top_names[i],
                     xy=(x, y),
                     xytext=(1.35 * np.sign(x), 1.4 * y),
                     horizontalalignment=horizontalalignment,
                     fontsize=16,
                     **kw)

    # 确保环形是一个正圆（否则会是椭圆）
    ax1.axis('equal')
    plt.title(f'{love_day}四天王（总{round(sum(sum_money), 1)}万）', fontsize=28)
    plt.text(0.25, 1.0, '数据来源：猫眼票房', fontsize=20, alpha=.7)
    pic_path2 = csv_file_path.replace('.csv', '环形图')  # 调整图片地址
    fig.savefig(f'{pic_path2}.png')  # 保存图像

    plt.show()
    print('程序处理完成！')


explain_data(r"D:\Study\Python\Spiders\猫眼电影\数据集\猫眼2024-04-22\2024-04-22.csv", '2024-04-22')