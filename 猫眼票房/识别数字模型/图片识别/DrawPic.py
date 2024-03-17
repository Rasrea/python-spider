from IdentifyPic import identify_pic
import os
import re
import matplotlib.pyplot as plt


# 配置字体地址
def draw_pic(name):
    woff_name = name.split('.')[0]
    t_path = os.path.dirname(__file__)
    file_path = os.path.join(t_path, '字体文件')
    woff_path = os.path.join(file_path, name)

    # 打开XML文件并以文本格式输出
    with open(woff_path, 'r') as file:
        xml_text = file.read()

    # 保存图片
    pic_file = os.path.join(t_path, f'图片集{woff_name}')
    os.makedirs(pic_file, exist_ok=True)  # 创建文件路径（如果不存在）

    # 找出XML文件中的加密信息
    pattern = re.compile(r'<TTGl.*?name="(uni.*?)".*?xMin=.*?>(.*?)</TTGlyph>', re.S)
    image = re.findall(pattern, xml_text)
    # 循环遍历每个加密信息
    for item in image:
        # 0 对应加密内容，1 对应解密内容
        x = [int(i) for i in re.findall(r'<pt x="(.*?)" y=', item[1])]
        y = [int(i) for i in re.findall(r'y="(.*?)" on=', item[1])]

        # 创建新的图像对象
        fig = plt.figure()
        plt.plot(x, y, color='black')
        plt.fill(x, y, color='black')  # 填充图形的内部
        plt.axis('off')  # 不显示坐标轴
        pic_path = os.path.join(pic_file, item[0] + '.png')
        fig.savefig(pic_path)

        # 关闭当前图像对象，以便下一次循环时创建新的图像对象
        # plt.show()
        plt.close()

    identify_pic(pic_file)  # 识别图像
