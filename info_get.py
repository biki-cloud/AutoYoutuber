import re


"""
<div class="thread">
<dl val="1" : "">
<dt class="idDs8X mesg hd " res="1"><a style="color:#000000" class="num" val="1" href="./1">1 ：<font color="#228811" class="name"><b>名無し</b></font></a>：23/10/01(日) 14:49:20 <span val="Ds8X" class="_id"><a class="id" rel="nofollow" val="Ds8X" href="/test/read.cgi/livejupiter/1696139360/?id=Ds8X">ID:Ds8X</a><a href="/test/read.cgi/livejupiter/1696139360/?q=主"><font size="2" color="red">主</font></a></span>
<dd class="idDs8X mesg body nusi_message" num="1">15歳でJリーグで活躍<br>19歳でリーガで試合出まくり<br>22歳で毎試合のように得点、ほぼ毎試合MOM、強豪ソシエダの絶対的エース<br>
</dd>
<ares num="1"></ares>
</dt>
</dl>
......
"""
def get_thread_info(dl):
    dl_val = dl['val']  # <dl val="1" :="">の値を取得
    dt = dl.find('dt')
    dd = dl.find('dd')

    # 必要な情報を抽出
    number = dl_val
    name = dt.find('font', class_='name').b.text
    pattern = r'\d{2}/\d{2}/\d{2}\(日\) \d{2}:\d{2}:\d{2}'
    # 正規表現にマッチする部分を抽出
    matches = re.findall(pattern, dt.text)

    if matches:
        datetime = matches[0]
    else:
        print("マッチする日付と時刻が見つかりませんでした。")
    ID = dt.find('a', class_='id').text
    if "ID:" in ID:
        ID = ID[3:]
    comment = dd.text.strip()

    # 結果をリストに追加
    return {
        "number": number,
        "name": name,
        "datetime": datetime,
        "ID": ID,
        "comment": comment
    }