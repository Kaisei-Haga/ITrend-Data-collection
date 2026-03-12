from google import genai
from google.genai import types
from src.config import GEMINI_API_KEY, GEMINI_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)

import json

def select_and_summarize(articles: list[dict]) -> list[dict]:
    articles_json = json.dumps(articles, ensure_ascii=False)
    
    prompt = f"""以下の記事リストから、技術者にとって価値のある記事を最大5件選定し、各記事を要約してください。

記事リスト:
{articles_json}

出力は以下のJSON形式のみで返してください。他の文章は一切含めないでください。

[
  {{
    "title": "記事タイトル",
    "url": "記事URL",
    "summary": "200文字以内の要約",
    "why_read": "100文字以内の読むべき理由"
  }}
]

要件:
- 最大10件
- summaryは200文字以内
- why_readは100文字以内
- 技術者向けの観点を含める
- JSON形式のみ出力"""

    for attempt in range(2):
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.2)
        )
        
        try:
            text = response.text.strip()
            text = text.replace("```json", "").replace("```", "").strip()
            result = json.loads(text)
            return result
        except json.JSONDecodeError:
            if attempt == 1:
                raise
    
    return []

def select_by_source(all_articles: list[dict]) -> list[dict]:
    """
    複数sourceの記事を受け取り、
    各sourceごとに最大5件Geminiで選定し、
    1つのlistにまとめて返す。
    """

    # ---------------------------
    # Step1: 空チェック
    # ---------------------------
    if not all_articles:
        return []

    # ---------------------------
    # Step2: sourceごとに分類
    # ---------------------------
    grouped: dict[str, list[dict]] = {}

    for article in all_articles:
        # sourceが無い場合はUnknown
        source = article.get("source", "Unknown")

        # groupedにsourceキーが無ければ空リストを作る
        if source not in grouped:
            grouped[source] = []

        grouped[source].append(article)

    # ---------------------------
    # Step3: 各sourceごとに選定
    # ---------------------------
    final_result: list[dict] = []

    for source, articles in grouped.items():

        # Geminiで選定（既存関数を使用）
        selected = select_and_summarize(articles)

        # 最大5件に制限
        selected = selected[:5]

        # 念のためsourceが欠けていたら補完
        for item in selected:
            if "source" not in item:
                item["source"] = source

        final_result.extend(selected)

    # ---------------------------
    # Step4: 結果を返す
    # ---------------------------
    return final_result