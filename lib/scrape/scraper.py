import requests
import os

class Scraper:
    def __init__(self) -> None:
        self.is_save = True
        pass

    def scrape(self, url: str, save_prefix) -> str:
        # scrape and return html content

        # HTTPリクエストを送信してHTMLを取得
        response = requests.get(url)
        html = response.text

        if self.is_save:
            html_save_dir = os.environ.get("HTML_SAVE_DIR")
            with open(os.path.join(html_save_dir, f"{save_prefix}_downloaded_content.html"), "w") as f:
                f.write(html)
        
        return html
