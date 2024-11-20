# マイポッドキャスト

このプロジェクトは、arXivの論文とRSSフィードからPodcastを生成します。arXivの検索結果とRSSフィードからPodcastを生成するように設計されています。ArXivやRSS提供先に負担がかからない範囲でご利用ください。


# 事前準備

## 必要なライブラリ

`Pipfile`を参照ください。

## gemini-1.5-flashの設定

`.env_sample`を参考に`.env`に`GOOGLE_API`を設定してください。

## 音声合成の準備

Podcastの音声合成には、VOICEVOX[^1]を使いました。VOICEVOX CORE[^2]を使ってAPIサーバーを立ち上げました。Windowsを使っている場合は、Windows版を実行すればおそらく問題なく動作するはずです。  音声合成APIのエンドポイントは環境変数`VICEVOX_API_URL`で指定します。

- GPUを使用するバージョン:
```bash
docker pull voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
docker run --rm --gpus all -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
```

### APIのURLや音声IDの変更

`podcast_audio.py`の設定を直接変更してください。  **APIのURLは環境変数`VICEVOX_API_URL`で指定されます。**
```python
# VICEVOX_API_URL = "http://localhost:50021"  <- .envファイルで設定
SPEACKER1_CHARACTOR_ID = 46
SPEACKER2_CHARACTOR_ID = 8
```

`.env`ファイルに`VICEVOX_API_URL`, `SPEACKER1_CHARACTOR_ID`, `SPEACKER2_CHARACTOR_ID`を設定してください。
`.env`ファイルの例：
```
VICEVOX_API_URL=http://localhost:50021
SPEACKER1_CHARACTOR_ID=46
SPEACKER2_CHARACTOR_ID=8
GOOGLE_API=YOUR_GOOGLE_API_KEY
```

# arXivからのPodcast生成

## 検索クエリの設定

`app/podcast.py`を変更してください:
```python
# 検索クエリを設定
input_search_query = "RAG Retrieval Augmented Generation"
category = "cat:cs"
```

## Podcastの生成
```bash
python app/podcast.py
```
これにより`podcast.wav`が生成されます。

# RSSからのPodcast生成

## URLの設定

`app/rss_podcast.py`を変更し、`url`変数を目的のRSSフィードに変更してください。

## Podcastの生成
```bash
python app/rss_podcast.py
```
プログラムの`url`変数を目的のRSSフィードに変更してください。


# 参考

- https://github.com/meta-llama/llama-recipes/tree/main/recipes/quickstart/NotebookLlama

# クレジット

- VOICEVOXは無料で使える中品質なテキスト読み上げ・歌声合成ソフトウェアです。
- https://voicevox.hiroshiba.jp/
- https://voicevox.hiroshiba.jp/term/

[^1]: https://voicevox.hiroshiba.jp/
[^2]: https://github.com/VOICEVOX/voicevox_engine
