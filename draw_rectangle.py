
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont

from ocr import Ocr, OcrTextInfoOnePage
from text_info import LineTextInfo, Pos


@dataclass
class Color():
    r: int
    g: int
    b: int

    def __iter__(self) -> Tuple[int, int, int]:
        return (self.r, self.g, self.b)

    def get_tuple(self) -> Tuple[int, int, int]:
        return (self.r, self.g, self.b)


def draw_rectangle(
        src_image: Image.Image,
        start_pos: Pos,
        end_pos: Pos,
        color: Color,
        fill: bool) -> Image.Image:

    draw: ImageDraw.ImageDraw = ImageDraw.Draw(src_image)

    draw.rectangle(
        (start_pos.get_tuple(),
         end_pos.get_tuple()),
        fill=(color.get_tuple() if fill else None),
        outline=color.get_tuple(),
        width=1)
    return src_image


def draw_rectangle_from_LineTextInfo(
    src_image: Image.Image,
    line_boxs: OcrTextInfoOnePage,
    color: Color = Color(255, 255, 255),
    fill: bool = False
) -> Image.Image:

    for line in line_boxs.texts:
        for word in line.text:
            draw_rectangle(
                src_image,
                word.start_pos,
                word.end_pos,
                color,
                fill)

    return src_image


def draw_string(
        src_image: Image.Image,
        start_pos: Pos,
        end_pos: Pos,
        strings: str,
        color: Color) -> Image.Image:
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(src_image)
    fontsize = 20
    fnt = ImageFont.truetype("C:\\Windows\\Fonts\\meiryob.ttc", fontsize)
    draw.text(start_pos.get_tuple(), strings, font=fnt,
              fill=color.get_tuple(),)
    return src_image


if __name__ == "__main__":
    def _main():
        image_path = "./image_file/test_01.png"
        ocr = Ocr()
        image = ocr.image_open(Path(image_path))
        image.show()

        result_ocr = ocr.extract(image)

        image_not_fill = draw_rectangle_from_LineTextInfo(
            image, result_ocr, Color(255, 0, 0), False)
        image_not_fill.show()

        image_fill = draw_rectangle_from_LineTextInfo(
            image, result_ocr, Color(255, 255, 255), True)
        image_fill.show()

        image3 = image_fill
        for line in result_ocr.texts:
            for word in line.text:
                draw_string(
                    image3,
                    word.start_pos,
                    word.end_pos,
                    word.text,
                    Color(255, 0, 0))

        image3.show()

    _main()
