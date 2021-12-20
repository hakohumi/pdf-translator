"""
Sample Python3 OAuthRequest
"""
import os
import requests as req
from requests_oauthlib import OAuth1
from configparser import ConfigParser
import json
import errno

from translator import Translator

# 入力は英語
# 出力は日本語


class TranslatorMinna(Translator):
    def __init__(self):
        config_ini = ConfigParser()

        config_ini_path = "./minna_api.ini"
        # 指定したiniファイルが存在しない場合、エラー発生
        if not os.path.exists(config_ini_path):
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(
                    errno.ENOENT), config_ini_path)

        config_ini.read(config_ini_path, encoding="utf-8")
        self.NAME = config_ini["API"]["NAME"]
        self.KEY = config_ini["API"]["KEY"]
        self.SECRET = config_ini["API"]["SECRET"]
        self.URL = "https://mt-auto-minhon-mlt.ucri.jgn-x.jp/api/mt/generalNT_en_ja/"

        self.consumer = OAuth1(self.KEY, self.SECRET)

    def translate(self, src_japanese: str) -> str:
        params = {
            'key': self.KEY,
            'name': self.NAME,
            "type": "json",
            "text": src_japanese
        }    # その他のパラメータについては、各APIのリクエストパラメータに従って設定してください。
        out_print: str = ""
        res = req.post(self.URL, data=params, auth=self.consumer)
        res.encoding = 'utf-8'
        # print(res)
        # print(res.text)

        result_json = {}

        try:
            result_json = json.loads(res.text)

        except Exception as e:
            print('=== Error ===')
            print('type:' + str(type(e)))
            print('args:' + str(e.args))
            print('e:' + str(e))
            raise e

        # ステータスコードの例外処理
        ret_code = result_json["resultset"]["code"]
        print(f"{ret_code=}")

        if ret_code == 531:
            raise Exception("翻訳サーバーがダウンしています。")

        # ------------------------

        # out_print: str = json.dumps(result_json, indent=2)
        out_print = result_json["resultset"]["result"]["text"]

        return out_print


if __name__ == "__main__":
    def _main():
        print(f"start {__file__} main")
        translator = TranslatorMinna()

        a = translator.translate("box")

        print(a)

    _main()
