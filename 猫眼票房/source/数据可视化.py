import pandas as pd
from matplotlib import pyplot as plt

# 配置环境
plt.style.use('seaborn-v0_8')  # 使用seaborn风格
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


# 存储文件信息，并进行可视化
def explain_data(csv_file_path, love_day):
    # 读取csv文件
    df = pd.read_csv(csv_file_path)
    columns = df.columns
    sum_money = [float(i) for i in df[columns[2]]]

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
    top_names = name_lst[:4]
    other_total = sum(all_money[4:])
    # 合并剩余的数据为一个“其他”类别
    top_money = all_money[:4] + [other_total]

    # 绘制饼图
    fig = plt.figure(figsize=(12, 8))  # 创建图像对象
    plt.pie(top_money, labels=top_names + ['其他'], autopct='%1.1f%%', textprops={'fontsize': 14})
    plt.title(f'{love_day}四大天王（总{round(sum(sum_money), 1)}万）', fontsize=18)  # 显示总票房，保留一位小数
    pic_path2 = csv_file_path.replace('.csv', '饼图')  # 调整图片地址
    fig.savefig(f'{pic_path2}.png')  # 保存图像

    plt.show()
    print('程序处理完成！')

