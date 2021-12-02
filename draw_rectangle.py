
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple
from PIL.Image import Image
from PIL.ImageDraw import ImageDraw, Draw
from pyocr.builders import LineBox
import cv2

from image_util import pil2cv
from ocr import Ocr
from text_info import LineTextInfo, Pos


# TODO: 文字列を図として貼り付けられる関数

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
        image: Image,
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
        src_image: Image,
        start_pos: Pos,
        end_pos: Pos,
        color: Color,
        fill: bool) -> Image:

    draw: ImageDraw = Draw(src_image)

    draw.rectangle(
        (start_pos.get_tuple(),
         end_pos.get_tuple()),
        fill=(color.get_tuple() if fill else None),
        outline=color.get_tuple())
    return src_image


def draw_rectangle_from_LineTextInfo_with_pillow(
        src_image: Image,
        line_boxs: list[LineTextInfo]) -> Image:

    for line in line_boxs:
        for word in line.text:
            draw_rectangle(
                src_image,
                word.start_pos,
                word.end_pos,
                Color(255, 255, 255),
                True)

    return src_image


def draw_rectangle_from_LineTextInfo(
        src_image: Image,
        line_boxs: list[LineTextInfo]) -> None:

    out = pil2cv(src_image)

    for line in line_boxs:
        for word in line.text:
            cv2.rectangle(out, word.start_pos.get_tuple(),
                          word.end_pos.get_tuple(), (0, 0, 255), 1)

        cv2.imshow("out", out)
        cv2.waitKey(0)


if __name__ == "__main__":
    def _main():
        image_path = "./image_file/test_01.png"
        ocr = Ocr()
        image = ocr.image_open(Path(image_path))
        image2 = draw_rectangle_from_LineTextInfo_with_pillow(
            image, ocr._text_info(image))
        image2.show()
        image3 = draw_rectangle_from_LineTextInfo_with_pillow(
            image2, ocr._text_info(image2))
        image3.show()

    _main()
