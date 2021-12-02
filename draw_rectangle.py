
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont
from pyocr.builders import LineBox
import cv2

from image_util import pil2cv
from ocr import Ocr
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


def draw_rectangle_from_LineBox(
        image: Image.Image,
        line_boxs: list[LineBox]) -> None:

    out = pil2cv(image)

    for line in line_boxs:
        line_string: str = ""
        for box in line.word_boxes:
            line_string += box.content + " "
            cv2.rectangle(
                out, box.position[0], box.position[1], (0, 0, 255), 1)

        print(line_string)
        cv2.imshow("out", out)
        cv2.waitKey(0)


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


def draw_rectangle_from_LineTextInfo_with_pillow(
    src_image: Image.Image,
    line_boxs: list[LineTextInfo],
    color: Color = Color(255, 255, 255),
    fill: bool = False
) -> Image.Image:

    for line in line_boxs:
        for word in line.text:
            draw_rectangle(
                src_image,
                word.start_pos,
                word.end_pos,
                color,
                fill)

    return src_image


def draw_rectangle_from_LineTextInfo(
        src_image: Image.Image,
        line_boxs: list[LineTextInfo]) -> None:

    out = pil2cv(src_image)

    for line in line_boxs:
        for word in line.text:
            cv2.rectangle(out, word.start_pos.get_tuple(),
                          word.end_pos.get_tuple(), (0, 0, 255), 1)

        cv2.imshow("out", out)
        cv2.waitKey(0)


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

        result_ocr = ocr._text_info(image)

        image_not_fill = draw_rectangle_from_LineTextInfo_with_pillow(
            image, result_ocr, Color(255, 0, 0), False)
        image_not_fill.show()

        image_fill = draw_rectangle_from_LineTextInfo_with_pillow(
            image, result_ocr, Color(255, 255, 255), True)
        image_fill.show()

        image3 = image_fill
        for line in result_ocr:
            for word in line.text:
                draw_string(
                    image3,
                    word.start_pos,
                    word.end_pos,
                    word.text,
                    Color(255, 0, 0))

        image3.show()

    _main()
