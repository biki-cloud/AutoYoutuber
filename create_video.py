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
    }
]

case = cases[0]

dryrun = True

if dryrun:
    # temp read html
    html_content = ""
    with open(case["save_html_path"], "r", encoding='utf-8') as f:
        html_content = f.read()
else:
    # scraper
    scraper = Scraper()
    html_content = scraper.scrape(case["url"], "test")

# get posts
thread = Thread(html_content)
posts = thread.get_posts()

# voice comment
voicebox = VoiceBox(logger)
wav_save_paths = []
comments = []
limits = 2
idx = 0
for post in posts:
    comments.append(post.comment)
    wav_save_paths.append(voicebox.text_to_voice(post.comment, f"{case['prefix']}_{post.index}"))
    idx += 1
    if idx >= limits:
        break

craete_movie(comments, wav_save_paths)

# 音声の合計時間を計算して、元動画の長さを増やす必要がある。リピートして。