import argparse
import json
import os
import time
from datetime import datetime

from tqdm import trange, tqdm

from dcinside import Crawler
from dcinside.exception import DeletedPostException, ServerException


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
    args = parser.parse_args()

    t = datetime.now()
    now = f"{t.year % 100}{t.month:02}{t.day:02}-{t.hour:02}{t.minute:02}{t.second:02}"
    file_name = f"{args.gallery}_{now}.json"

    if not os.path.isdir("data"):
        os.mkdir("data")

    crawler = Crawler(args.driver, timeout=60, retry=True)
    count = 0

    data = []

    for post_idx in trange(args.start_idx, args.end_idx + 1):
        try:
            post = crawler.crawl(args.gallery, post_idx)
            # print(post["title"])
            # print(post["content"])
            comments = []
            for comment in post["comments"]:
                comment = comment.rstrip(" - dc App").strip()
                comment = comment.replace("\n", " ")
                comments.append(comment)

            d = {
                "title": post["title"].strip(),
                "content": post["content"].strip(),
                "comments": comments,
            }

            data.append(d)

        except (ServerException, DeletedPostException) as e:
            tqdm.write(f"{args.gallery} {post_idx} {e}")

        time.sleep(0.6)

    # 파일 저장
    total_data = len(data)
    total_comments = sum(len(d["comments"]) for d in data)
    json_data = {
        "gallery": args.gallery,
        "total_data": total_data,
        "total_comments": total_comments,
        "data": data,
    }

    with open(os.path.join("data", file_name), "w", encoding="utf-8") as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)
        print(f"파일 저장: {os.path.join('data', file_name)}")

    print(f"완료, 크롤링한 글 수: {total_data}, 댓글 수: {total_comments}")
