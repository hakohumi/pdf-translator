"""
Sample Python3 OAuthRequest
"""
import os
import requests as req
from requests_oauthlib import OAuth1
from configparser import ConfigParser
import json
import errno

config_ini = ConfigParser()

config_ini_path = "./minna_api.ini"
# 指定したiniファイルが存在しない場合、エラー発生
if not os.path.exists(config_ini_path):
    raise FileNotFoundError(
        errno.ENOENT, os.strerror(
            errno.ENOENT), config_ini_path)

config_ini.read(config_ini_path, encoding="utf-8")
NAME = config_ini["API"]["NAME"]
KEY = config_ini["API"]["KEY"]
SECRET = config_ini["API"]["SECRET"]
URL = "https://mt-auto-minhon-mlt.ucri.jgn-x.jp/api/mt/generalNT_en_ja/"


consumer = OAuth1(KEY, SECRET)

params = {
    'key': KEY,
    'name': NAME,
    "type": "json",
    "text": "hello"
}    # その他のパラメータについては、各APIのリクエストパラメータに従って設定してください。

try:
    res = req.post(URL, data=params, auth=consumer)
    res.encoding = 'utf-8'
    print("[res]")
    print(res)
    # print(res.text)

    result_json: dict = json.loads(res.text)

    print(json.dumps(result_json, indent=2))

except Exception as e:
    print('=== Error ===')
    print('type:' + str(type(e)))
    print('args:' + str(e.args))
    print('e:' + str(e))
