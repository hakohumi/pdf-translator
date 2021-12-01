# 入力:画像データ
# 出力:文字列

from pathlib import Path
from typing import Text
from PIL import Image as pil
from PIL.Image import Image
from pyocr.tesseract import image_to_string
from pyocr.builders import LineBox, LineBoxBuilder
from pyocr.pyocr import get_available_tools

from text_info import LineTextInfo


# PDFが何単語あるのか、調査する
# 1ページ 3110文字
# 3110文字 * 2180ページ = 約600万文字


class Ocr:
    """
    文章が描かれた画像データから文字列を抽出する
    入力： 画像データ
    出力： 文字列
    """

    def __init__(self) -> None:
        pass

    def image_open(self, image_path: Path) -> Image:
        return pil.open(image_path)

    def extract(self, image: Image):
        text_info_list: list[LineTextInfo] = self._text_info(image)
        return text_info_list

    def _text_info(self, image: Image) -> list[LineTextInfo]:
        line_boxs = image_to_string(
            image,
            lang="eng",
            builder=LineBoxBuilder(tesseract_layout=6)
        )

        if not isinstance(line_boxs, list):
            print(line_boxs)
            print(type(line_boxs))
            raise Exception("line_boxsがlistではありません。")

        for line in line_boxs:
            if not isinstance(line, LineBox):
                print(line)
                print(type(line))
                raise Exception("未対応のエラーです")

        line_text_info_list: list[LineTextInfo] = []
        for line in line_boxs:
            line_box_info: LineTextInfo = LineTextInfo.generate_from_LineBoxList(
                line)
            line_text_info_list.append(line_box_info)
        return line_text_info_list


if __name__ == "__main__":
    import sys

    def _main():
        # コマンドライン引数で、ディレクトリを指定する
        tools = get_available_tools()
        if len(tools) == 0:
            print("No OCR tool found")
            sys.exit(1)

        tool = tools[0]

        print("Will use tool '%s'" % (tool.get_name()))

        image_path = "./image_file/test_01.png"

        ocr = Ocr()
        image: Image = ocr.image_open(Path(image_path))
        output_string = ocr.extract(image)

        for line in output_string:
            print(len(line), str(line))

        print(f"total strings = {sum([len(line) for line in output_string])}")
    _main()
