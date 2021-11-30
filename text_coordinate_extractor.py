
from pathlib import Path
from PIL.Image import Image
from PIL import Image as pil
from pyocr.tesseract import image_to_string
from pyocr.builders import LineBox, LineBoxBuilder
import cv2

from image_util import pil2cv


class TextCoordinateExtractor:
    """
    画像の中から文章のまとまり（座標）を抽出する
     入力： 画像データ
     出力： 文章座標のリスト
    """

    def __init__(self) -> None:
        pass

    def image_open(self, image_path: Path) -> Image:
        return pil.open(image_path)

    def extract(self, image: Image) -> None:

        out = pil2cv(image)
        line_boxs = image_to_string(
            image,
            lang="eng",
            builder=LineBoxBuilder(tesseract_layout=6)
        )

        for line in line_boxs:
            if not isinstance(line, LineBox):
                print(line)
                print(type(line))
                raise Exception("未対応のエラーです")

            line_string: str = ""
            for box in line.word_boxes:
                # print(box.position)
                # print(box.content)
                line_string += box.content + " "
                cv2.rectangle(
                    out, box.position[0], box.position[1], (0, 0, 255), 1)

            print(line_string)
            cv2.imshow("out", out)
            cv2.waitKey(0)
            # TODO: wip:戻り値未実装


if __name__ == "__main__":
    def _main():
        text_coordinater = TextCoordinateExtractor()
        image_path = "./image_file/test_01.png"

        text_coordinater.extract(text_coordinater.image_open(Path(image_path)))

    _main()
