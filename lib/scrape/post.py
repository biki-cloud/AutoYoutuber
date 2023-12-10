from bs4 import BeautifulSoup, ResultSet
import bs4

class Post:
    def __init__(self, data: bs4.element.Tag):
        self.index: str = ""
        self.name: str = ""
        self.date: str = ""
        self.time: str = ""
        self.id: str = ""
        self.comment: str = ""

        self.parse_data(data)
    
    def parse_data(self, data: bs4.element.Tag):
        """
        postをパースして、各プロパティに格納する
        """
        dt_text = data.get_text()
        dt_texts = dt_text.split("：")

        self.index = dt_texts[0].strip()
        self.name = data.find('b').get_text()
        comment = data.find('dd').get_text().split("\n")[0]
        self.comment = comment.replace("  ", "\n")

        splited_content = dt_texts[2].split(" ")
        self.date = splited_content[0]
        self.time = splited_content[1]
        temp_comment = splited_content[2]
        self.id = temp_comment[:temp_comment.find(self.comment)][3:]

    def default_post(self) -> str:
        """
        return default post like below
        ---
        47 ：名無しさん：2020/11/19(木) 08:27:06.27 ID:ImDbcoyn.net
        ジョコ次勝てばいいにしても
        ティエム→メドベ？となったら体力尽きそう
        ---
        """
        return f"{self.index} ：{self.name}：{self.date} {self.time} ID:{self.id}\n{self.comment}"