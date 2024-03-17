from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import os


# 灰度化函数
def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])


# 识别图像
def identify_pic(file_path):
    # 获取文件名
    name_pic = [i.split('.')[0] for i in os.listdir(file_path)]

    # 读取图像并转换为灰度图像
    test_images = []  # 数据集
    for item in name_pic:
        image = plt.imread(os.path.join(file_path, item + '.png'))
        gray_image = rgb2gray(image)  # 灰度处理
        test_images.append(gray_image)

    # 预处理数据
    test_images = np.array(test_images)
    test_images = test_images.reshape((10, 480 * 640)).astype('float32') / 255

    # 调用模型
    loaded_model = keras.models.load_model(r"猫眼图像识别.keras")
    # 使用加载的模型进行预测
    predictions = loaded_model.predict(test_images)

    # 转化为字典
    num_data = {key: value.argmax() for key, value in zip(name_pic, predictions)}
    print(f'long: {len(num_data)}')
    print(num_data)
