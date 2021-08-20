import argparse
import csv
import os
import time
from datetime import datetime

from tqdm import trange

from dcinside import Crawler
from dcinside.exception import *


parser = argparse.ArgumentParser()
parser.add_argument("gallery", type=str, help="갤러리의 이름")
parser.add_argument("start_idx", type=int, help="크롤링을 시작할 글 번호")
parser.add_argument("end_idx", type=int, help="크롤링을 끝낼 글 번호")
parser.add_argument(
    "--driver",
    type=str,
    help="selenium이 사용할 크롬 드라이버의 경로",
    default="./chromedriver",
)

if __name__ == "__main__":
    t = datetime.now()
    now = f"{t.year % 100}{t.month:02}{t.day:02}-{t.hour:02}{t.minute:02}{t.second:02}"
    file_name = f"{now}.csv"

    if not os.path.isdir("data"):
        os.mkdir("data")

    file = open(os.path.join("data", file_name), "w", encoding="utf-8", newline="")
    writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["content", "label"])

    args = parser.parse_args()
    crawler = Crawler(args.driver, timeout=60, retry=True)
    count = 0

    for post_idx in trange(args.start_idx, args.end_idx + 1):
        try:
            post = crawler.crawl(args.gallery, post_idx)
            # print(post["title"])
            # print(post["content"])
            for comment in post["comments"]:
                comment = comment.rstrip(" - dc App").strip()
                comment = comment.replace("\n", " ")
                # print(comment)
                if 3 <= len(comment) <= 256:
                    writer.writerow([comment, 0])
                    count += 1
        except (ServerException, DeletedPostException) as e:
            print(args.gallery, post_idx, e)
        time.sleep(0.873)

    file.close()
    print(f"완료, 크롤링한 댓글 수: {count}")
