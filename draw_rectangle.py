
from pathlib import Path
from PIL.Image import Image
from pyocr.builders import LineBox
import cv2

from image_util import pil2cv
from ocr import Ocr
from text_info import LineTextInfo


def draw_rectangle(image: Image, line_boxs: list[LineBox]) -> None:

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


def draw_rectangle2(image: Image, line_boxs: list[LineTextInfo]) -> None:

    out = pil2cv(image)

    for line in line_boxs:
        for word in line.text:
            cv2.rectangle(
                out, word.start_pos.get_tuple(), word.end_pos.get_tuple(), (0, 0, 255), 1)

        cv2.imshow("out", out)
        cv2.waitKey(0)


if __name__ == "__main__":
    def _main():
        image_path = "./image_file/test_01.png"
        ocr = Ocr()
        image = ocr.image_open(Path(image_path))
        draw_rectangle2(image, ocr._text_info(image))

    _main()
