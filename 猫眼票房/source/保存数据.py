from 数据可视化 import explain_data
import csv
import os


# 导入csv文件
def keep_data(combine_money, part_money, film_name, release_time, love_day):
    # 定义列名
    headers = ['排名', '名称', '当日（综合）票房（万）', '当日（分账）票房（万）', '上映时间（天）']

    # 定义文件保存地址
    t_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 绝对地址
    file_path = os.path.join(t_path, '数据集', f'猫眼{love_day}')
    os.makedirs(file_path, exist_ok=True)    # 创建文件路径（如果不存在）
    csv_file_path = os.path.join(file_path, f'{love_day}.csv')

    # 将列表按竖列写入CSV文件
    with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(headers)  # 写入列名

        # 写入数据，并增加排名
        for i, row in enumerate(zip(film_name, combine_money, part_money, release_time), start=1):
            writer.writerow([i] + list(row))
    print(f'数据保存在（{csv_file_path}）')
    explain_data(csv_file_path, love_day)
