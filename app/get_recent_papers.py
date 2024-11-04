import arxiv
import pandas as pd
from arxiv import UnexpectedEmptyPageError
import os
import markdown

def get_arxiv_abstruct(query):
    # arxiv.Clientをインスタンス化します。
    client = arxiv.Client()

    # 検索条件を設定します。
    search = arxiv.Search(
        query=query,
        max_results=100,  # 取得する論文の最大件数を指定します。
        # sort_by=arxiv.SortCriterion.Relevance #関連度順でダウンロード
        sort_by=arxiv.SortCriterion.SubmittedDate #日付でダウンロード
    )

    # 検索を実行し、結果を取得します。
    results = []
    try:
        for result in client.results(search): # client.results()を使用
            results.append({
                "title": result.title,
                "abstract": result.summary,
                #Bibtexを生成するために必要な情報を追加
                'authors': result.authors,
                'published': result.published,
                'journal_ref': result.journal_ref,
                'entry_id': result.entry_id
            })
    except UnexpectedEmptyPageError as e:
        # エラーが発生した場合、エラーメッセージと発生したURLを表示します
        print(f"Error: {e}")
        print(f"URL: {e.url}")
        # 処理を継続するか、終了するかを決定します
        # ここでは、エラーが発生したページをスキップして処理を継続します

    return results


def generate_bibtex(result):
    # BibTeX形式の引用を生成する関数
    authors = " and ".join([author.name for author in result['authors']])
    title = result['title']
    year = result['published'].year
    if result['journal_ref'] is not None:
        journal = result['journal_ref']
    else:
        journal = result['entry_id']
    bibtex = (
          f"@article{{{result['entry_id']}}},\n"
          f"author = {{{authors}}},\n"
          f"title = {{{title}}},\n"
          f"journal = {{{journal}}},\n"
          f"year = {{{year}}}\n"
          "}"
      )
    return bibtex

def search_arxiv(input_search_query, category = "cat:cs", num_papers = 100):
    # Arxiv APIを使用して論文を検索します。

    search_query = category + " " + input_search_query
    # query = "High Entropy alloy"
    # query_date = "submittedDate:[{} TO {}]"
    results = get_arxiv_abstruct(search_query)

    # BibTeX形式の引用を結果に追加します。
    for result in results:
        result["bibtex"] = generate_bibtex(result)

    # データフレームに変換します。
    df = pd.DataFrame(results)
    # title, abstract, bibtexだけのDataFrameを作成します。
    df = df[["title", "abstract", "bibtex"]]

    return df


def save_abst(df, base_filename, save_path = "./output"):
    # 分割してmarkdownとして保存します。
    # 初期
    max_chars = 50000 # NotebookLMの1ファイルあたりの許容文字数
    current_chars = 0
    file_number = 1
    html_content = ""
    to_markdown = True
    os.makedirs(save_path, exist_ok=True)

    for index in range(len(df)):
        content = f"""# Title: {df["title"][index]}
    ## abstract
    {df["abstract"][index]}
    ## bibtex
    {df['bibtex'][index]}
    """
        if to_markdown == True:
            html_entry = content
            ext = ".md"
        else:
            html_entry = markdown.markdown(content)
            ext = ".html"

        entry_length = len(html_entry)

        if current_chars + entry_length > max_chars:
            # If character limit is exceeded, save current content and start a new file
            with open(f"{save_path}/{base_filename}_part{file_number}{ext}", "w") as f:
                f.write(html_content)
            print(f"{base_filename}_part{file_number}{ext} saved.")

            file_number += 1
            html_content = ""  # Reset for the new file
            current_chars = 0

        html_content += html_entry
        current_chars += entry_length

    # Save the remaining content to the last file
    if html_content:
        with open(f"{save_path}{base_filename}_part{file_number}{ext}", "w") as f:
            f.write(html_content)
        print(f"{base_filename}_part{file_number}{ext} saved.")

    print("HTML/md content split and saved into multiple files.")

if __name__ == "__main__":
    # 文字列を検索してCSVファイルに保存します。
    input_search_query = "RAG Retrieval-Augmented Generation"
    df = search_arxiv(input_search_query = input_search_query)
    df.to_csv("./output/arxiv_papers.csv", index=False)
    print("データセットが 'arxiv_papers.csv' として保存されました。")
    base_filename = "Papers_about_" + input_search_query.replace(" ", "_")
    save_abst(df, base_filename, save_path = "./output")
