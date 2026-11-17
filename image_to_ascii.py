from PIL import Image
from io import BytesIO

def image_to_ascii(image_data: bytes, wight: int = 160) -> str:
    image =Image.open(BytesIO(image_data))

    old_width,old_height = image.size;
    height = max(1, int(old_height / old_width * width * 0.5) );

    image = image.resize((width, height)).convert("L");


    """
    将图片转换为 ASCII 字符画
    :param image_data: 图片的二进制数据
    :param wight: 输出的宽度，默认 160
    :return: ASCII 字符画字符串
    """
    # 打开图片
    image = Image.open(BytesIO(image_data))

    # 原来的宽高
    old_width, old_height = image.size

    # 字符不是正方形，所以高度要缩小一些
    height = int(old_height / old_width * wight * 0.5)

    # 缩小图片
    image = image.resize((wight, height))

    # 转成灰度
    image = image.convert("L")

    # 从亮到暗
    chars = "@%#*+=-:. "

    # 生成 ASCII
    result = ""

    for y in range(height):
        for x in range(wight):

            # 获取这个位置的亮度
            brightness = image.getpixel((x, y))

            # 亮度 0~255
            # 转换成 chars 的位置
            if brightness > 240:
                result += " "
            else:
                index = brightness * (len(chars) - 1) // 255
                result += chars[index]

        result += "\n"

    return result

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