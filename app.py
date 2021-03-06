from pathlib import Path
import sys

from PIL.Image import Image
from draw_rectangle import Color, draw_rectangle_from_LineTextInfo, draw_string
from ocr import Ocr, TextInfoOnePage

from pdf_to_image import convert_pdf_to_png
from text_info import TextInfoLine
from translator_minna import TranslatorMinna


if __name__ == "__main__":
    def _file_search(search_files_path: Path) -> list[Path]:
        out_files_path: list[Path] = []
        out_files_path = list(search_files_path.glob("*.png"))
        return out_files_path

    def _main():
        # pdfを画像ファイルとして入力
        args = sys.argv

        if len(args) == 2:
            pdf_path = Path(args[1])
        else:
            raise Exception("PDFファイルのパスを指定してください。")

        dist_image_path = Path("./image_file")
        convert_pdf_to_png(pdf_path, dist_image_path)
        image_file_paths: list[Path] = _file_search(dist_image_path)

        for image_file_path in image_file_paths:

            # 画像ファイルから文字列を取得
            ocr = Ocr()
            pict_file_path: Path = image_file_path
            image: Image = ocr.image_open(pict_file_path)
            image.show()

            result_ocr: TextInfoOnePage = ocr.extract(image)
            print(f"単語数:{len(result_ocr)}, 文字数: {result_ocr.get_len_words()}")
            image_fill_white = draw_rectangle_from_LineTextInfo(
                image, result_ocr, Color(255, 255, 255), True)

            # TODO: 1ページを段組ごとに分けて翻訳する
            # TODO: 段組単位で単語、行を文章へ変換する
            # TODO: 翻訳
            translator = TranslatorMinna()
            translated_texts: list[TextInfoLine] = []
            for line in result_ocr.texts:
                translated_word_text: str = translator.translate(str(line))
                print(f"{translated_word_text}")
                translated_line_text_info: TextInfoLine = TextInfoLine(
                    line.start_pos, line.end_pos, line.text, translated_word_text)
                translated_texts.append(translated_line_text_info)
            one_page_text_info = TextInfoOnePage(translated_texts)

            for line in one_page_text_info.texts:
                if line.translated_text is not None:
                    draw_string(
                        image_fill_white,
                        line.start_pos,
                        line.end_pos,
                        line.translated_text,
                        Color(255, 0, 0))

            image_fill_white.show()

    _main()
