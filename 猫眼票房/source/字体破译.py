import re


# 破译字体文件
def beat_data(xml_text):
    # 找出XML文件中的加密信息
    pattern = re.compile(r'<TTGl.*?name="(uni.*?)".*?xMin=.*?>(.*?)</TTGlyph>', re.S)
    image_text = re.findall(pattern, xml_text)
    # 将加密信息按字符'contour'个数分类
    two_count = []
    one_count = []
    key_thr = {}  # 以字典的形式存储破解信息

    # 循环遍历每个加密信息
    for i, str_text in enumerate(image_text):
        count_text = re.findall(r'<contour>', str_text[1])
        # 分别存放在各自的列表中
        if len(count_text) == 3:
            key_thr[str_text[0]] = 8
        elif len(count_text) == 2:
            two_count.append(str_text)
        else:
            if i == len(image_text):  # 排除最后一个
                break
            else:
                one_count.append(str_text)

    # 根据图像数据的行数进一步区分列表中的值
    line_dict = {}
    list_two = [9, 6, 0, 4]
    for data in two_count:
        line_count = data[1].count('\n') + 1
        line_dict[data[0]] = line_count

    # 使用sorted函数对字典的键值对进行排序，根据值进行排序，reverse参数设置为True表示降序
    key_two = dict(sorted(line_dict.items(), key=lambda item: item[1], reverse=True))

    # 使用循环遍历使解码结果分别对应4
    for key, value in zip(key_two.keys(), list_two):
        key_two[key] = value

    # 区分数字9和6，比较第二部分y坐标的大小
    # 获取字典的键列表
    keys = list(key_two.keys())
    nin_text = ''  # 初始化
    six_text = ''
    for text in image_text:
        if text[0] == keys[0]:
            nin_text = text
        if text[0] == keys[1]:
            six_text = text

    # 获得数字9第二部分y坐标值和
    sec_nin_text = re.search('</cont.*?tour>(.*?)</contour>', nin_text[1], re.S).group(1)
    nin_y = [int(i) for i in re.findall(r'y="(.*?)" on=', sec_nin_text)]
    # 同理得数字6
    sec_six_text = re.search('</cont.*?tour>(.*?)</contour>', six_text[1], re.S).group(1)
    six_y = [int(i) for i in re.findall(r'y="(.*?)" on=', sec_six_text)]

    # 比较第二部分y坐标的值的总和
    if sum(nin_y) < sum(six_y):
        # 9, 6需要调换
        keys = list(key_two.keys())[:2]  # 获取字典中的前两个键
        key_two[keys[0]], key_two[keys[1]] = 6, 9

    # 同理破译另一部分
    line_dict = {}
    list_one = [3, 2, 5, 7, 1]
    for data in one_count:
        line_count = data[1].count('\n') + 1
        line_dict[data[0]] = line_count
    key_one = dict(sorted(line_dict.items(), key=lambda item: item[1], reverse=True))
    for key, value in zip(key_one.keys(), list_one):
        key_one[key] = value

    # 合并成解码字典
    key_dict = {**key_thr, **key_two, **key_one}

    return key_dict  # 返回破译字符
