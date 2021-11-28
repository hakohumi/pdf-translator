# 入力:画像データ
# 出力:文字列

from PIL import Image
import sys
from pyocr.tesseract import image_to_string
from pyocr.builders import LineBox, LineBoxBuilder
from pyocr.pyocr import get_available_tools, TOOLS

# TODO: 座標が正しく取得できているのかを確認したい
# 取得できた座標の位置に点を描画させる
# 出力：元の画像データの上から点を描画し、新しい画像ファイルとして作成する

if __name__ == "__main__":
    def _main():
        # コマンドライン引数で、ディレクトリを指定する
        tools = get_available_tools()
        if len(tools) == 0:
            print("No OCR tool found")
            sys.exit(1)

        tool = tools[0]

        print("Will use tool '%s'" % (tool.get_name()))

        line_boxs = image_to_string(
            Image.open("./image_file/test_01.png"),
            lang="eng",
            builder=LineBoxBuilder(tesseract_layout=6)
        )

        for line in line_boxs:
            if not isinstance(line, LineBox):
                raise Exception("未対応のエラーです")

            # print(line)
            # print(line.content)
            print(line.word_boxes)
            pass

    _main()
