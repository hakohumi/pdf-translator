# Python Pdf Translator

## 概要

PDFファイルを翻訳するサービス

## 使用方法

翻訳したいpdfファイルを指定すると、翻訳されたファイルが作成される

## 要件仕様

- 英語を日本語に翻訳する
- 翻訳前と翻訳後の文字列の位置は変わらない
- 翻訳はどのサービスを使用しても良い
- 1つのpdfファイルの翻訳を1タスクとし、複数のタスクを予約としてスタックすることができる。

## 流れ

1. pdfファイルを画像化する
1. 画像をORCを使用し、英文と座標を抽出する
1. 英文を翻訳し、日本語に変換する
1. 元の座標の範囲を白く塗りつぶし、翻訳した日本語を貼り付ける
1. pdf、または画像ファイルとして出力する

## 要素技術

- Python
- PDF to 画像ファイル
  - pdf2image
  - poppler
    - pdf2imageが依存する外部ライブラリ
    - Windows: `https://blog.alivate.com.au/poppler-windows/`
    - 解凍してそのままプロジェクトディレクトリに追加する
- ORC
  - https://itport.cloud/?p=8326
  - Tesseract
    - インストール時に日本語用のスクリプトと言語を追加する設定を入れる
    - Tesseractのインストールディレクトリ`C:\Program Files\Tesseract-OCR`にパスを通しておく
    - 環境変数`TESSDATA_PREFIX`に`C:\Program Files\Tesseract-OCR\tessdata`を追加する
  - PyOCR
    - poetry add pyocr
- 英語 to 日本語 翻訳API
- PDFファイル操作
  - 読み込み、書き込み
  - オブジェクトの挿入
    - テキスト
    - 図形

## pdf_to_imgage

pdfをpngへ変換する

pdfファイルのパスを指定する
もしくは、pdfファイルが入っているディレクトリを指定する

## ocr

画像データから英字文字列と座標を抽出する

入力： 画像データ
出力： 英字文字列と文字列の座標

## 
