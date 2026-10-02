from PIL import Image

# ====== 你只需要改这里 ======

image_file = "naiwa.png"   # 图片文件名
width = 80                # ASCII 最终宽度

# 从亮到暗
chars = "@%#*+=-:. "

# ============================


# 打开图片
image = Image.open(image_file)

# 原来的宽高
old_width, old_height = image.size

# 字符不是正方形，所以高度要缩小一些
height = int(old_height / old_width * width * 0.5)

# 缩小图片
image = image.resize((width, height))

# 转成灰度
image = image.convert("L")


# 生成 ASCII
result = ""

for y in range(height):
    for x in range(width):

        # 获取这个位置的亮度
        brightness = image.getpixel((x, y))

        # 亮度 0~255
        # 转换成 chars 的位置
                # 白色背景直接变成空格
        if brightness > 240:
            result += " "
        else:
            index = brightness * (len(chars) - 1) // 255
            result += chars[index]
            
    result += "\n"


# save
with open("ascii.txt", "w", encoding="utf-8") as file:
    file.write(result)

print("success!")
print(f"width：{width}")
print("file：ascii.txt")