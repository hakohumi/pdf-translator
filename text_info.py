from dataclasses import dataclass
from typing import Optional

from pyocr.builders import LineBox


@dataclass
class Pos:
    x: int
    y: int

    def get_tuple(self):
        return (self.x, self.y)


@dataclass
class Word:
    text: str
    start_pos: Pos
    end_pos: Pos

    def __str__(self):
        return self.text

    def __len__(self):
        return len(self.text)


@dataclass
class TextInfoLine:
    """
     文章情報
    """
    start_pos: Pos
    end_pos: Pos
    text: list[Word]
    translated_text: Optional[str]

    def __str__(self) -> str:
        a = [str(word) for word in self.text]
        return " ".join(a)

    def get_len_words(self) -> int:
        return len(self.text)

    def __len__(self) -> int:
        return len(str(self))

    @staticmethod
    def generate_from_LineBoxList(line_box: LineBox) -> "TextInfoLine":
        texts: list[Word] = []

        for box in line_box.word_boxes:
            start_pos: Pos = Pos(box.position[0][0], box.position[0][1])
            end_pos: Pos = Pos(box.position[1][0], box.position[1][1])
            texts.append(Word(box.content, start_pos, end_pos))

        line_text_info: TextInfoLine = TextInfoLine(
            texts[0].start_pos, texts[0].end_pos, texts, None
        )

        return line_text_info


# TODO: OCRクラスにカプセル化させる

@dataclass
class TextInfoOnePage:
    texts: list[TextInfoLine]

    def show(self):
        for line in self.texts:
            print(len(line), str(line))
        print(f"total strings = {sum([len(line) for line in self.texts])}")

    def get_len_words(self):
        return sum([len(word_len) for word_len in self.texts])

    def __len__(self):
        return len(([len(line) for line in self.texts]))
