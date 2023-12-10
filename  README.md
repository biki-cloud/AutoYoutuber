# 自動でyoutubeに動画を投稿するアプリ

## 要件定義
- 自動でyoutubeに動画を投稿したい
- 2ちゃんねるのスレッド内容を動画にする
- 音声をつけたい
- [手本のyoutuber](https://www.youtube.com/@garuch-matome/featured)


## 設計
- とりあえず簡単な動画を作成 -> youtubeにアップロードするまでをやってみる。
- 動画から音を動画に入れる必要があル。
  - 音源を作成
  - テロップを入れる。
  - 動画に合わせる

### スクレイピング
- スクレイプできるか。
- 多分途中でスクレイピングできなくなる可能性。一日一回スクレイピングしたい

### 音声
- 音声はvoiceboxで何種類かの音声を再現できる。

### 動画
- 動画編集はmoviepyとかやってみる。

### Youtube投稿
- APIで投稿する

### ディレクトリ構成
- lib/voice: 音声ライブラリ
- lib/scrape: スクレイピングライブラリ
- lib/movie: 動画ライブラリ
- lib/youtube: youtubeライブラリ
- lib/creater: ライブラリを使用して動画作成 -> youtube投稿を行う
- app.py: 実行するファイル

### その他
- requirements.txtの作成