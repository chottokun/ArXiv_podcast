from get_recent_papers import search_arxiv, save_abst
from create_podcast_scenario import load_markdown, summarize_text, write_podcast
from podcast_audio import save_audio, combine_wav_files
import tempfile
from dotenv import load_dotenv
import os
import json
import ast

# 検索文字列をセット
input_search_query = "RAG Retrieval Augmented Generation"
category = "cat:cs"

# 検索と念ためのデータ保存
df = search_arxiv(input_search_query = input_search_query, category = category)
df.to_csv("./output/arxiv_papers.csv", index=False)
print("データセットが 'arxiv_papers.csv' として保存されました。")

# markdownにする。
with tempfile.TemporaryDirectory() as temp_dir:
    base_filename = "Papers"
    save_abst(df, base_filename, save_path = temp_dir)
    text = load_markdown(file_path = f"{temp_dir}/{base_filename}_part1.md")

# 要約
summary = summarize_text(text, input_search_query)
# podcastのシナリオを作成
scenario = write_podcast(summary)
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