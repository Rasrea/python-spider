import re
import matplotlib.pyplot as plt

# 打开XML文件并以文本格式输出
with open('20a70494.woff.xml', 'r') as file:
    xml_text = file.read()

# 找出XML文件中的加密信息
pattern = re.compile(r'<TTGl.*?name="(uni.*?)".*?xMin=.*?>(.*?)</TTGlyph>', re.S)
image = re.findall(pattern, xml_text)

# 循环遍历每个加密信息
for item in image:
    # 0 对应加密内容，1 对应解密内容
    print(item[0])
    x = [int(i) for i in re.findall(r'<pt x="(.*?)" y=', item[1])]
    y = [int(i) for i in re.findall(r'y="(.*?)" on=', item[1])]

    # 创建新的图像对象
    plt.figure()
    plt.plot(x, y)
    plt.fill(x, y, color='black')  # 填充图形的内部

    '''# 保存绘制的图像并设置边距为0
    plt.savefig(item[0], bbox_inches='tight', pad_inches=0)'''
    # 关闭当前图像对象，以便下一次循环时创建新的图像对象
    plt.show()
    plt.close()
