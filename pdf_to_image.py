import os
import sys
from pathlib import Path
from pdf2image import convert_from_path

# poppler/binを環境変数PATHに追加する
poppler_dir = Path(__file__).parent.absolute() / "poppler/bin"
os.environ["PATH"] += os.pathsep + str(poppler_dir)


# TODO: 出力されるファイル名のルールを明記する

def convert_pdf_to_png(pdf_path: Path, dist_image_path: Path):
    # PDF -> Image に変換（150dpi）
    pages = convert_from_path(str(pdf_path), 200)

    # 画像ファイルを１ページずつ保存
    for i, page in enumerate(pages):
        file_name = pdf_path.stem + "_{:02d}".format(i + 1) + ".png"
        image_path = dist_image_path / file_name

        print(image_path)
        # JPEGで保存
        page.save(str(image_path), "PNG")


if __name__ == "__main__":
    def _main():
        args = sys.argv

        if len(args) == 2:
            pdf_path = Path(args[1])
        else:
            raise Exception("PDFファイルのパスを指定してください。")

        dist_image_path = Path("./image_file")

        convert_pdf_to_png(pdf_path, dist_image_path)

    _main()
