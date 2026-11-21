from io import BytesIO
from pathlib import Path
import sys

from PIL import Image


CHARS = "@%#*+=-:. "

def image_to_ascii(
    image_data: bytes,
    width: int = 160,
    gamma: float = 1.0,
    contrast: float = 1.0,
) -> str:

def adjust_brightness(
    brightness: int,
    gamma: float = 1.0,
    contrast: float = 1.0,
) -> int:
    normalized = brightness / 255

    corrected = normalized ** gamma

    adjusted = (corrected - 0.5) * contrast + 0.5

    return round(max(0, min(1, adjusted)) * 255)


def image_to_ascii(image_data: bytes, width: int = 160) -> str:
    """Convert image bytes into an ASCII-art string."""
    if width < 20 or width > 300:
        raise ValueError("width must be between 20 and 300")

    with Image.open(BytesIO(image_data)) as source:
        old_width, old_height = source.size
        if old_width <= 0 or old_height <= 0:
            raise ValueError("image dimensions must be positive")

        height = max(1, int(old_height / old_width * width * 0.5))
        image = source.convert("L").resize((width, height))

    result = []
    for y in range(height):
        line = []
        for x in range(width):
            brightness = adjust_brightness(
            image.getpixel((x, y)),
            gamma,
            contrast,
)

            if brightness > 240:
                line.append(" ")
            else:
                index = brightness * (len(CHARS) - 1) // 255
                line.append(CHARS[index])

        result.append("".join(line).rstrip())

    return "\n".join(result)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 image_to_ascii.py IMAGE [WIDTH]")
        raise SystemExit(1)

    image_path = Path(sys.argv[1])
    if not image_path.is_file():
        print(f"Image not found: {image_path}")
        raise SystemExit(1)

    try:
        width = int(sys.argv[2]) if len(sys.argv) >= 3 else 160
        ascii_art = image_to_ascii(image_path.read_bytes(), width)
    except (ValueError, OSError) as error:
        print(f"Could not convert image: {error}")
        raise SystemExit(1)

    sys.stdout.write(ascii_art)


if __name__ == "__main__":
    main()
