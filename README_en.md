# my-podcast

This project generates podcasts from arXiv papers and RSS feeds.  This project is designed to generate podcasts from arXiv search results and RSS feeds. Please use this within the limits that do not burden arXiv or RSS providers.


# Prerequisites

## Required Libraries

See `Pipfile`.

## Setting up gemini-1.5-flash

Refer to `.env_sample` and set `GOOGLE_API` in `.env`.

## Voice Synthesis Setup

VOICEVOX[^1] is used for podcast voice synthesis. I used VOICEVOX CORE[^2] to set up the API server. If you're on Windows, running the Windows version should work.

- For GPU versions:
```bash
docker pull voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
docker run --rm --gpus all -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
```

### Changing API URL or Voice ID

Modify the settings in `podcast_audio.py` directly.
```python
VICEVOX_API_URL = "http://localhost:50021"
SPEACKER1_CHARACTOR_ID = 46
SPEACKER2_CHARACTOR_ID = 8
```

# Generating from ArXiv

## Setting Search Query

Modify `app/podcast.py`:
```python
# Set search query
input_search_query = "RAG Retrieval Augmented Generation"
category = "cat:cs"
```

## Podcast Generation
```bash
python app/podcast.py
```
This will generate `podcast.wav`.

# Generating from RSS

## Setting URL

Modify `app/rss_podcast.py` and change the `url` variable to your desired RSS feed.

## Podcast Generation
```bash
python app/rss_podcast.py
```
Change the `url` variable in the program to your desired RSS feed.


# References

- https://github.com/meta-llama/llama-recipes/tree/main/recipes/quickstart/NotebookLlama

# Credits

- VOICEVOX is free, medium-quality text-to-speech and singing voice synthesis software.
- https://voicevox.hiroshiba.jp/
- https://voicevox.hiroshiba.jp/term/

[^1]: https://voicevox.hiroshiba.jp/
[^2]: https://github.com/VOICEVOX/voicevox_engine
