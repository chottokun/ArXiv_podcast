# ArXivから検索した論文をまとめてPodcast
検索文字列などなどハードコーディングしたままです。ArXiv運営に負担がかからない範囲でご利用ください。

# 事前準備

## 必要必ブラリ
Pipfileを参照ください。

## gemini-1.5-flashの利用準備
.env_sampleを参考に.envにGOOGLE_APIをセットしてください。

## 音声合成準備
Podcastの音声合成には、VOICEVOX[^1]を使いました。私は、VOCEVOX CORE[^2]にてAPIサーバを立ち上げました。Windowsならwindows版を立ち上げておけば、おそらく大丈夫だと思います。

- GPUありのバージョンの場合は以下。
```
docker pull voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
docker run --rm --gpus all -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
```

### APIのURLや音声IDを変更させたい場合。
podcast_audio.py中の設定を直接書き換えます。
```
VICEVOX_API_URL = "http://localhost:50021"
SPEACKER1_CHARACTOR_ID = 46
SPEACKER2_CHARACTOR_ID = 8
```

# 検索文字列セット

app/podcast.pyを書き換え下さい。
```Python 
# 検索文字列をセット
input_search_query = "RAG Retrieval Augmented Generation"
category = "cat:cs"
```

# RSSからPodcast
```Python 
python app/rss_podcast.py
```
上記プログラムのurlを好きなRSSのフィードに書き換えてください。

# 参考
- https://github.com/meta-llama/llama-recipes/tree/main/recipes/quickstart/NotebookLlama

# クレジット
- VOICEVOXは無料で使える中品質なテキスト読み上げ・歌声合成ソフトウェアです。
- https://voicevox.hiroshiba.jp/
- https://voicevox.hiroshiba.jp/term/

[^1]: https://voicevox.hiroshiba.jp/
[^2]: https://github.com/VOICEVOX/voicevox_engine
