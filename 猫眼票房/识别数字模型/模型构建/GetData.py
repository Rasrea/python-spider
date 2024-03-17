import os
import numpy as np
import matplotlib.pyplot as plt


# 获取训练数据
def get_data():
    train_images = []
    file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 绝对地址
    folder_path = os.path.join(file_path, '训练集')  # 合成文件地址
    files_lst = os.listdir(folder_path)  # 读取所有文件名
    for item in files_lst:
        pic_path = os.path.join(folder_path, item)  # 合成完整地址
        image = plt.imread(pic_path)  # 转化为矩阵
        train_images.append(image)
    train_images = np.array(train_images)  # 转化为数组类型

    # 获取数据标签
    train_labels = [int(i.split('_')[0]) for i in files_lst]
    train_labels = np.array(train_labels)

    # 获取测试数据
    test_images = []
    folder_path = os.path.join(file_path, '测试集')  # 合成文件地址
    files_lst = os.listdir(folder_path)

    for item in files_lst:
        pic_path = os.path.join(folder_path, item)
        image = plt.imread(pic_path)

        test_images.append(image)
    test_images = np.array(test_images)

    # 获取测试标签
    test_labels = [int(i.split('_')[0]) for i in files_lst]
    test_labels = np.array(test_labels)

    return train_images, train_labels, test_images, test_labels
