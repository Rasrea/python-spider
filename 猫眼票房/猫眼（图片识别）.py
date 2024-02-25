from PIL import Image
import pytesseract
import matplotlib.pyplot as plt


captcha = Image.open("uniE583.png")

img = captcha.convert("L")  # 处理灰度
pixels = img.load()
# 二值化处理
for x in range(img.width):
    for y in range(img.height):
        if pixels[x, y] > 150:
            pixels[x, y] = 255
        else:
            pixels[x, y] = 0

result = pytesseract.image_to_string(img)
print(result)