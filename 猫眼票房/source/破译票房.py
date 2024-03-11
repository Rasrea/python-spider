from 字体破译 import beat_data
import os
import re


# 破解票房数据
def get_boxs(key_dict, movie_list):
    # 获取当前文件夹路径
    folder_path = os.path.dirname(os.path.realpath(__file__))
    files_path = os.path.join(folder_path, '字体文件')
    # 获取当前文件夹中的所有文件，如果字体更新，则遍历其他字体
    files = os.listdir(files_path)

    # 解析票房（综合及分账）数据
    combine_money = []  # 存储综合票房
    part_money = []  # 存储分账票房
    for item in movie_list:
        # 初始化票房数据
        t_con_money = ''
        t_par_money = ''

        # 提取（综合）票房信息，转为大写、替换字符、转换成列表
        combine_text = item['boxSplitUnit']['num'].upper().replace('&#X', 'uni')
        combine_lst = re.findall(r'(uni.*?);', combine_text)  # 转化成列表，方便之后遍历
        # 提取（分账）票房信息，同上
        part_text = item['splitBoxSplitUnit']['num'].upper().replace('&#X', 'uni')
        part_lst = re.findall(r'(uni.*?);', part_text)

        # 如果字体文件与数据文件不匹配，则更改字体文件
        if not all(key in key_dict for key in combine_lst):
            # 过滤出 XML 文件
            xml_files = [file for file in files if file.endswith('.xml')]
            # 遍历字体文件，直达符合后返回
            for x_file in xml_files:
                with open(os.path.join(files_path, x_file), 'r') as f:  # 补全地址
                    xml_text = f.read()  # 读取数据后重新返回破译函数

                # 再次开始破译
                key_dict = beat_data(xml_text)
                if all(key in key_dict for key in combine_lst):
                    break  # 如果字符全部匹配，则破译成功，返回破译字典

        # 遍历转换（综合）票房并存储
        for i in combine_lst:  # 将字符串相互对比、转化
            t_con_money = t_con_money + str(key_dict[i])
        t_con_money = float(t_con_money) / 100  # 保留两位小数
        combine_money.append(t_con_money)
        # （分账）票房同上
        for j in part_lst:
            t_par_money = t_par_money + str(key_dict[j])
        t_par_money = float(t_par_money) / 100
        part_money.append(t_par_money)

    return combine_money, part_money
