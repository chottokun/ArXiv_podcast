import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

def build_model(API_KEY):
    generation_config = {
    "temperature": 0.1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
    }
    model_name = 'gemini-1.5-flash-latest'
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(
        model_name,
        generation_config=generation_config,
        )
    return model


def summarize_text(text, input_search_query):

  my_prompt = f"""<Inputs>
<search_query>{input_search_query}</search_query>
</Inputs>
<Instructions Structure>
1. まず、{input_search_query}に関する論文のリストを受け取ります。
2. 次に、そのリストをもとに最近の技術傾向を要約します。
3. 最後に、要約を大学生でも分かりやすいように日本語で提供します。
</Instructions Structure>
<Instructions>
以下の内容に従って、{input_search_query}に関する最近の技術傾向をまとめてください。
提供された論文のリストを読み、各論文の主要な技術的進展やトレンドを特定します。
特定したトレンドを基に、最近の技術傾向について簡潔に要約します。
最後に、その要約を日本語で記述してください。
論文のリストは以下の通りです：
<論文リスト>
{text}
</論文リスト>
</Instructions>
"""

  response = model.generate_content(my_prompt)
  return response.text


def write_podcast(text):
    Transcript_PROMPT = f"""
    You are the a world-class podcast writer.
    <Inputs>
    # ポッドキャストの内容
    {text}
    </Inputs>
    <Instructions>
    あなたは世界的に有名なテクニカルポッドキャストライターです。
    あなたの仕事は、InputsされたテキストについてSpeaker 2のあいづちも含めて会話を書くことです。
    非常に楽しく多くの技術内容に詳しい会話を含みます。
    英語はカタカナで表記します。
    Inputsされたテキストの内容をすべて盛り込みます。
    話者は時折脱線しますが、トピックについて議論を続ける必要があります。

    以下の指示に従ってください：
    - 最初にSpeaker 1のダイアログから始めてください。
    - 次に、興奮や好奇心を示すSpeaker 2のダイアログを追加してください。
    - 説明の中で素晴らしい逸話や比喩を提供し、会話を引き立ててください。
    - Speaker 2には「うーん」、「あー」、「はあ」などのあいづちを挿入し、中断を加えてください。
    - 応答は厳密にダイアログ形式で返してください。エピソードタイトルや章タイトルは別に提供しないでください。

    応答の例:
    [
    ("Speaker 1", "我々のポッドキャストへようこそ。エーアイと技術の最新の進歩について探求します。ホストの赤坂です。今日は、エーアイ分野の著名な専門家をお迎えしています。メタ エーアイからの最新リリース、ラマ 3.2の魅力的な世界に飛び込みましょう。"),
    ("Speaker 2", "こんにちは、ここにいられてとても嬉しいです！ラマ 3.2とは何ですか？"),
    ("Speaker 1", "いい質問ですね！ラマ 3.2はオープンソースのエーアイモデルで、開発者がどこでもエーアイモデルを微調整、蒸留、展開できるようにします。前のバージョンからの大きなアップデートで、パフォーマンス、効率、カスタマイズオプションが向上しています。"),
    ("Speaker 2", "それは素晴らしいですね！ラマ 3.2の主な特徴は何ですか？")
    ]
    </Instructions>
    """

    response = model.generate_content(Transcript_PROMPT)
    #print(response.text)
    try:
        return json.dumps(json.loads(response.text), ensure_ascii=False, indent=4)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return "[]"


def load_markdown(file_path = "./output/test.md"):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return ""

def save_podcast_scenario(podcast_json, save_path="output/"):
    with open(f"{save_path}podcast_data.json", 'w') as f:
        json.dump(podcast_json, f, ensure_ascii=False, indent=4)

# initial
load_dotenv()
model = build_model(API_KEY = os.environ["GOOGLE_API_KEY"])


if __name__ == "__main__":
    # .envファイルの内容を読み込見込む
    load_dotenv()
    API_KEY = os.environ["GOOGLE_API_KEY"]
    #text = load_markdown(file_path = "./output/podcast.md") #コメントアウト
    # モデルを定義
    model = build_model(API_KEY)
    # 要約
    #summary = summarize_text(text, "RAG") #コメントアウト
    # podcastのシナリオを作成
    response = write_podcast("test") # テスト用のテキスト
    # podcastを保存
    save_podcast_scenario(response)
