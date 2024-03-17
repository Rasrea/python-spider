from GetData import get_data
from tensorflow import keras
from tensorflow.keras import layers


def pic_model():
    train_images, train_labels, test_images, test_labels = get_data()

    # 数据预处理
    train_images = train_images.reshape((2500, 480 * 640)).astype('float32') / 255
    test_images = test_images.reshape((1357, 480 * 640)).astype('float32') / 255

    # 构建模型
    model = keras.Sequential([
        layers.Dense(512, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])

    # 编译模型
    model.compile(optimizer='rmsprop',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    # 训练模型
    model.fit(train_images, train_labels, epochs=3, batch_size=50)  # 迭代3次

    # 保存模型
    model.save("猫眼图像识别.keras")

    # 加载模型
    loaded_model = keras.models.load_model("猫眼图像识别.keras")
    # 使用加载的模型进行预测
    print('\n评测数据：')
    text_loss, test_acc = loaded_model.evaluate(test_images, test_labels)
    print(f'test_acc: {test_acc}')
