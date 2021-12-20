# 入力:画像データ
# 出力:文字列

from pathlib import Path
from PIL import Image as pil
from PIL.Image import Image
import pyocr.tesseract as TES
from pyocr.builders import LineBox, LineBoxBuilder
from pyocr.pyocr import get_available_tools

from text_info import TextInfoLine, TextInfoOnePage


# PDFが何単語あるのか、調査する
# 1ページ 3110文字
# 3110文字 * 2180ページ = 約600万文字

# TODO: 内部で変動する情報を持たない、イミュータブルにする
# TODO: OCRしたあとは別のインスタンスを作成し返すようにする
# TODO: 内部で画像データ、文字列を持つ


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
        return TextInfoOnePage(self._text_info(image))

    def _text_info(self, image: Image) -> list[TextInfoLine]:
        line_boxs = TES.image_to_string(
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

        line_text_info_list: list[TextInfoLine] = []
        for line in line_boxs:
            line_box_info: TextInfoLine = TextInfoLine.generate_from_LineBoxList(
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

        output_string.show()

    _main()
