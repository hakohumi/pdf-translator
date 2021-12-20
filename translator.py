# TODO: 翻訳API インターフェース
# どのAPIでも共通して使用できるように、抽象化する

from abc import ABCMeta, abstractmethod


# TODO: 非同期で実行できるようにする

class Translator(metaclass=ABCMeta):

    @abstractmethod
    def translate(self, src_japanese: str) -> str:
        """
        translate 英文を日本語に翻訳する
        """
        print("interface")
        return ""
