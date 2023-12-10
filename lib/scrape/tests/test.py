from bs4 import BeautifulSoup, ResultSet
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'test.html'), 'r', encoding='utf-8') as file:
    html_content = file.read()

# BeautifulSoupを使用して<title>タグの内容を取得する
soup = BeautifulSoup(html_content, 'html.parser')
title_content = soup.title.string

# 結果を出力する
print("title: " + title_content)

dt_tags: ResultSet = soup.find_all('dt')

for dt in dt_tags:
    print("*" * 20)
    print(type(dt))
    dt_text = dt.get_text()
    dt_texts = dt_text.split("：")

    index = dt_texts[0].strip()
    name = dt.find('b').get_text()
    comment = dt.find('dd').get_text().split("\n")[0]
    comment = comment.replace("  ", "\n")

    splited_content = dt_texts[2].split(" ")
    date = splited_content[0]
    time = splited_content[1]
    temp_comment = splited_content[2]
    print(comment)

    d = {
        "index": index,
        "name": name,
        "id": temp_comment[:temp_comment.find(comment)][3:],
        "date": date,
        "time": time,
        "comment": comment
    }

    print(d)
