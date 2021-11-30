# 入力:画像データ
# 出力:文字列

from pathlib import Path
from PIL import Image as pil
from PIL.Image import Image
from pyocr.tesseract import image_to_string
from pyocr.builders import LineBox, LineBoxBuilder
from pyocr.pyocr import get_available_tools


# TODO: PDFが何単語あるのか、調査する

# TODO: 単語で情報を持つようにする
# 文字と座標を持つ（pyocrからのデータそのままでもいい）


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
        text_info = self._text_info(image)
        if not isinstance(text_info, list):
            raise Exception("未対応", type(text_info))
        return self._join_strings(text_info)

    def _text_info(self, image: Image) -> list[LineBox]:
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

        return line_boxs

    def _join_strings(self, line_boxs: list[LineBox]):
        ret_string: list[str] = []

        for line in line_boxs:

            line_string: str = ""
            for box in line.word_boxes:
                line_string += box.content + " "
            ret_string.append(line_string)

        return ret_string


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
        print("\n".join(output_string))

    _main()
