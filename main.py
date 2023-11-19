from bs4 import BeautifulSoup
import json
import requests
from info_get import get_thread_info

# スクレイピング対象のURL
url = "https://hayabusa.open2ch.net/test/read.cgi/livejupiter/1696139360/l10"

# HTTPリクエストを送信してHTMLを取得
response = requests.get(url)
html = response.text
print(html)

# with open("downloaded_content.html", "rb") as f:
#     html = f.read()

# BeautifulSoupを使用してHTMLをパース
soup = BeautifulSoup(html, "html.parser")

# タイトルを取得
title = soup.title.text.strip()

# <div class="thread">要素内のすべての<dl>要素を取得
thread_div = soup.find('div', class_='thread')
dl_elements = thread_div.find_all('dl')

threads = []
# <dl>要素を処理
for dl in dl_elements:
    threads.append(get_thread_info(dl))

# JSONデータを作成
data = {
    "html_file_url": url,
    "title": title,
    "threads": threads
}

# 結果を表示
json_data = json.dumps(data, ensure_ascii=False, indent=4)
print(json_data)