from rss_paser_llm import rss_parser
from create_podcast_scenario import write_podcast
from podcast_audio import save_audio, combine_wav_files
import tempfile
import json
import ast

url = "https://www.nhk.or.jp/rss/news/cat0.xml"
max_articles  = 10
rss_contents, _ = rss_parser(url=url, max_articles=max_articles)
# podcastのシナリオを作成
scenario = write_podcast(rss_contents)
# json変換
podcast_json = json.dumps(scenario, ensure_ascii=False, indent=4)
loaded_data = json.loads(podcast_json)
# dictへ
loaded_data = ast.literal_eval(loaded_data)
# audio変換
with tempfile.TemporaryDirectory() as temp_dir:
# print(temp_dir)
    save_audio(loaded_data, temp_dir)
    combine_wav_files("podcast.wav", temp_dir)