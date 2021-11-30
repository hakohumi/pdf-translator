
from pathlib import Path
from PIL.Image import Image
from pyocr.builders import LineBox
import cv2

from image_util import pil2cv
from ocr import Ocr


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


if __name__ == "__main__":
    def _main():
        image_path = "./image_file/test_01.png"
        ocr = Ocr()
        image = ocr.image_open(Path(image_path))
        draw_rectangle(image, ocr._text_info(image))

    _main()
