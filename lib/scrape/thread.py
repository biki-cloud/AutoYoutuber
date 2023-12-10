from bs4 import BeautifulSoup, ResultSet

from lib.scrape.post import Post

class Thread:
    """
    implements below methods and properties
    properties:
        title: thread title
        url: thread url
    methods:
        get_posts: return list of Post object
    """
    def __init__(self, html_content: str):
        self.soup = BeautifulSoup(html_content, "html.parser")
        self.title = self.soup.title.get_text()
    
    def get_posts(self) -> list:
        """
        return list of Post object
        """
        dt_tags: ResultSet = self.soup.find_all('dt')
        posts = []
        for dt in dt_tags:
            posts.append(Post(dt))
        return posts