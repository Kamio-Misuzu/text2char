"""


                                      @@                                   @@
     @    @@                          @@                    @@        @@   @@
     @    @                                                 @@       @@@
     @   @@                                                 @@@      @@@
     @  @@     @@@@    @@ @@@  @@@@   @@    @@@@            @ @      @@@   @@   @@@@   @@    @@  @@@@@@ @@    @@
     @ @@      @  @@   @@@  @@@@ @@   @@   @@  @@@          @ @@    @@ @   @@  @@  @   @@    @@      @@ @@    @@
     @@@           @@  @@    @@   @@  @@  @@    @@          @  @    @  @   @@  @@      @@    @@     @@  @@    @@
     @@@          @@@  @@    @    @@  @@  @@     @          @  @   @@  @   @@  @@      @@    @@     @   @@    @@
     @ @@      @@  @@  @@    @    @@  @@  @      @  @@@@@   @  @@  @   @   @@   @@@    @@    @@    @@   @@    @@
     @  @@    @    @@  @@    @    @@  @@  @      @          @   @ @@   @   @@     @@   @@    @@   @@    @@    @@
     @   @@   @    @@  @@    @    @@  @@  @@    @@          @   @@@    @   @@      @@  @@    @@   @     @@    @@
     @    @@  @@  @@@  @@    @    @@  @@   @@  @@           @    @@    @   @@  @   @    @@  @@@  @@      @@  @@@
     @     @@  @@@ @@  @@    @    @@  @@    @@@@            @    @     @   @@  @@@@      @@@ @@ @@@@@@@   @@@ @@

"""


from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os


def text_to_hash_art(
        text,
        font_path=None,
        font_size=20,
        threshold=128,
        char="#",
        bg_char=" ",
        output_width=None,
        fix_bottom_cut=True,
        margin=3
):
# 可以根据路径C:/Windows/Fonts来查看自己有哪些字体(Windows下)
    if font_path is None:
        font_candidates = [
            "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
            "C:/Windows/Fonts/simhei.ttf",  # 黑体
            "/System/Library/Fonts/STHeiti Medium.ttc",  # Mac黑体
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"  # Linux
        ]
        for path in font_candidates:
            if os.path.exists(path):
                font_path = path
                break
        else:
            raise FileNotFoundError("未找到系统字体，请手动指定 font_path")

    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError as e:
        raise ValueError(f"字体加载失败: {e}")

    temp_img = Image.new("L", (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    bbox = temp_draw.textbbox((0, 0), text, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    if fix_bottom_cut:
        ascent, descent = font.getmetrics()
        text_height += max(descent, margin)

    img_width = text_width + 2 * margin
    img_height = text_height + 2 * margin
    img = Image.new("L", (img_width, img_height), color=255)
    draw = ImageDraw.Draw(img)
    draw.text((margin, margin), text, font=font, fill=0)

    img_array = np.array(img)
    if output_width and output_width < img_width:
        from skimage.transform import resize
        scale = output_width / img_width
        img_array = resize(
            img_array,
            (int(img_height * scale), output_width),
            anti_aliasing=False
        )
        img_array = (img_array * 255).astype(np.uint8)


    result_text = "\n".join(
        "".join(char if pixel < threshold else bg_char for pixel in row)
        for row in img_array
    )

    return result_text


if __name__ == "__main__":
    print(text_to_hash_art("Kamio-Misuzu", font_size=16, char="@"))

