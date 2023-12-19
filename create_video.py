import os
import logging

from lib.scrape.thread import Thread
from lib.scrape.scraper import Scraper
from lib.voice.voicebox import VoiceBox
from lib.movie.movie import craete_movie


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
# create fomatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# set fomatter to stream handler
logger.handlers[0].setFormatter(formatter)

html_save_dir = os.environ.get("HTML_SAVE_DIR")

cases = [
    {
        "prefix": "tennis",
        "save_html_path": os.path.join(html_save_dir, "tennis.html"),
        "url": "https://hayabusa5.2ch.sc/test/read.cgi/dome/1605728861/0-"
    },
    {
        "prefix": "employee",
        "save_html_path": os.path.join(html_save_dir, "employee.html"),
        "url": "https://nozomi.2ch.sc/test/read.cgi/employee/1462624724/0-"
    },
    {
        "prefix": "news4vip",
        "save_html_path": os.path.join(html_save_dir, "news4vip.html"),
        "url": "https://nozomi.2ch.sc/test/read.cgi/be/1575083477/"
    }
]

case = cases[2]

is_scrape = False

if is_scrape:
    # temp read html
    logger.info("read html...")
    html_content = ""
    with open(case["save_html_path"], "r", encoding='utf-8') as f:
        html_content = f.read()
else:
    # scraper
    logger.info("scrape start...")
    scraper = Scraper()
    html_content = scraper.scrape(case["url"], "test")

# get posts
thread = Thread(html_content)
posts = thread.get_posts()

# voice comment
voicebox = VoiceBox(logger)
wav_save_paths = []
comments = []
# どのくらいのコメントを読み、動画を作成するか
limits = 100
idx = 0
for post in posts:
    comments.append(post.default_post())
    wav_save_paths.append(voicebox.text_to_voice(post.comment, f"{case['prefix']}_{post.index}"))
    idx += 1
    if idx >= limits:
        break

craete_movie(comments, wav_save_paths, logger)
