# Python Pdf Translator

## 概要

PDFファイルを翻訳するサービス

## 使用方法

翻訳したいpdfファイルを指定すると、翻訳されたファイルが作成される

TODO: 最終的なパッケージとしての使い方、実行環境の構築の流れなどを記載する

## 要件仕様

- 英語を日本語に翻訳する
- 翻訳前と翻訳後の文字列の位置は変わらない
- 翻訳はどのサービスを使用しても良い
- 1つのpdfファイルの翻訳を1タスクとし、複数のタスクを予約としてスタックすることができる。

## 流れ

1. [x] pdfファイルを画像化する
2. [x] 画像にORCを使用し、英文と座標を抽出する
3. [ ] 英文を翻訳し、日本語に変換する
4. [ ] 元の座標の範囲を白く塗りつぶし、翻訳した日本語を貼り付ける
5. [ ] pdf、または画像ファイルとして出力する

## 要素技術

TODO: 上の流れと同じような構成にする、モジュール単位

- Python
  - 3.9.6
- PDF to 画像ファイル
  - pdf2image
  - poppler
    - pdf2imageが依存する外部ライブラリ
    - Windows: `https://blog.alivate.com.au/poppler-windows/`
    - 解凍してそのままプロジェクトディレクトリに追加する
- ORC
  - <https://itport.cloud/?p=8326>
  - Tesseract
    - インストール時に日本語用のスクリプトと言語を追加する設定を入れる
    - Tesseractのインストールディレクトリ`C:\Program Files\Tesseract-OCR`にパスを通しておく
    - 環境変数`TESSDATA_PREFIX`に`C:\Program Files\Tesseract-OCR\tessdata`を追加する
  - PyOCR
    - poetry add pyocr
- 英語 to 日本語 翻訳API
  - [みんなの自動翻訳＠TexTra®](https://mt-auto-minhon-mlt.ucri.jgn-x.jp/content/menu/)
    - プロジェクトのルートに、「minna_api.ini」ファイルを作成する必要がある。
      - 中には、
        - セクション名: API
        - キー: NAME, KEY, SECRET
- PDFファイル操作
  - 読み込み、書き込み
  - オブジェクトの挿入
    - テキスト
    - 図形

## pdf_to_imgage

pdfをpngへ変換する

pdfファイルのパスを指定する
もしくは、pdfファイルが入っているディレクトリを指定する

popplerのライブラリを使用するため、解凍したバイナリのライブラリのディレクトリを
プロジェクトルートに「poppler」というディレクトリ名で配置する。

## ocr

画像データから英字文字列と座標を抽出する

入力： 画像データ
出力： 英字文字列と文字列の座標
