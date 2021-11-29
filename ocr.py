# 入力:画像データ
# 出力:文字列

from PIL import Image
import sys
from pyocr.tesseract import image_to_string
from pyocr.builders import LineBox, LineBoxBuilder, TextBuilder
from pyocr.pyocr import get_available_tools, TOOLS
import cv2

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
        image_path = "./image_file/test_01.png"
        line_boxs = image_to_string(
            Image.open(image_path),
            lang="eng",
            builder=LineBoxBuilder(tesseract_layout=6)
        )
        out = cv2.imread(image_path)

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

    _main()
