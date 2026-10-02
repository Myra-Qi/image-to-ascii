from pathlib import Path
import sys


# =========================
# 配置
# =========================

# 输出宽度
TARGET_WIDTHS = [120, 160, 200]

# 字符亮度表
# 从亮 -> 暗
CHARS = " .:-=+*#%@"


# =========================
# 读取文件
# =========================

if len(sys.argv) < 2:
    print("用法：")
    print("  python3 resize_ascii.py ascii.txt")
    sys.exit(1)

input_file = Path(sys.argv[1])

if not input_file.exists():
    print(f"找不到文件：{input_file}")
    sys.exit(1)

text = input_file.read_text(encoding="utf-8")

# 保留每一行
lines = text.splitlines()

if not lines:
    print("文件是空的。")
    sys.exit(1)


# =========================
# 1. 去掉完全空白的行
# =========================

lines = [line.rstrip("\n\r") for line in lines]

# 找到真正有内容的行
non_empty = [line for line in lines if line.strip()]

if not non_empty:
    print("文件里面没有找到有效 ASCII 内容。")
    sys.exit(1)

# 上下裁剪
first = next(i for i, line in enumerate(lines) if line.strip())
last = len(lines) - 1 - next(
    i for i, line in enumerate(reversed(lines)) if line.strip()
)

lines = lines[first:last + 1]


# =========================
# 2. 左右裁剪
# =========================

# 左侧最小缩进
left = min(
    len(line) - len(line.lstrip(" "))
    for line in lines
    if line.strip()
)

# 左侧统一裁掉
lines = [line[left:] for line in lines]

# 找到最右边真正有内容的位置
right = max(
    len(line.rstrip())
    for line in lines
)

# 右侧统一裁掉
lines = [line[:right] for line in lines]


original_width = max(len(line) for line in lines)
original_height = len(lines)

print()
print("原始 ASCII：")
print(f"  宽度：{original_width}")
print(f"  高度：{original_height}")
print()


# =========================
# 补齐每一行
# =========================

lines = [
    line.ljust(original_width)
    for line in lines
]


# =========================
# ASCII 降采样
# =========================

def resize_ascii(lines, target_width):
    """
    将 ASCII 字符画缩小到指定宽度。
    """

    src_height = len(lines)
    src_width = len(lines[0])

    # 宽度缩放比例
    scale_x = src_width / target_width

    # 字符通常比实际像素“高”，
    # 所以高度需要额外压缩。
    #
    # 这个值可以调整：
    # 0.5 -> 更矮
    # 0.6 -> 中等
    # 0.7 -> 更高
    aspect_correction = 0.55

    target_height = max(
        1,
        round(src_height / scale_x * aspect_correction)
    )

    result = []

    for y in range(target_height):

        # 对应原图中的 y
        src_y = min(
            src_height - 1,
            int(y * src_height / target_height)
        )

        source_line = lines[src_y]

        new_line = []

        for x in range(target_width):

            src_x = min(
                src_width - 1,
                int(x * src_width / target_width)
            )

            new_line.append(source_line[src_x])

        result.append("".join(new_line).rstrip())

    return result


# =========================
# 生成多个尺寸
# =========================

for width in TARGET_WIDTHS:

    result = resize_ascii(lines, width)

    output_file = input_file.with_name(
        f"{input_file.stem}_{width}.txt"
    )

    output_file.write_text(
        "\n".join(result),
        encoding="utf-8"
    )

    print(
        f"生成：{output_file.name}"
        f"  ({width} × {len(result)})"
    )


print()
print("。。。")
print("：")
print()

for width in TARGET_WIDTHS:
    print(f"  {input_file.stem}_{width}.txt")