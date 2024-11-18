import feedparser
import os

def rss_parser(url, max_articles = 10):
    f = feedparser.parse(url)
    f['entries'] = f['entries'][:max_articles]
    output_str = ""
    for article in f['entries'][:max_articles]:  # 変数を使用してスライス
        output_str += f"# {article['title']}\n\n"
        output_str += f"{article['summary']}\n\n"
    os.makedirs("./output", exist_ok=True) # ディレクトリが存在しない場合に作成
    with open("./output/podcast.md", "w", encoding="utf-8") as f:
        f.write(output_str)
    return(output_str, f)

if __name__ == "__main__":
    url = "https://rss.itmedia.co.jp/rss/2.0/itmedia_all.xml"
    max_articles = 10
    output, _ = rss_parser(url=url)
    print(output)
