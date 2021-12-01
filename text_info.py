from dataclasses import dataclass

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
class LineTextInfo:
    """
     文章情報
    """
    text: list[Word]
    start_pos: Pos
    end_pos: Pos

    def __str__(self) -> str:
        a = [str(word) for word in self.text]
        return " ".join(a)

    def __len__(self) -> int:
        return len(str(self))

    @staticmethod
    def generate_from_LineBoxList(line_box: LineBox) -> "LineTextInfo":
        texts: list[Word] = []

        for box in line_box.word_boxes:
            start_pos: Pos = Pos(box.position[0][0], box.position[0][1])
            end_pos: Pos = Pos(box.position[1][0], box.position[1][1])
            texts.append(Word(box.content, start_pos, end_pos))

        line_text_info: LineTextInfo = LineTextInfo(
            texts, Pos(0, 0), Pos(0, 0))

        return line_text_info
