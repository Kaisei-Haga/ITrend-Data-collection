def generate_html(hn_articles: list[dict], hatena_articles: list[dict], qiita_articles: list[dict]) -> str:
    html_parts = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "<meta charset='UTF-8'>",
        "<title>Tech Articles</title>",
        "<style>",
        "body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f7fa;}",
        "h1 { color: #333; }",
        "h2 { color: #666; border-bottom: 2px solid #ddd; padding-bottom: 10px; margin-top: 40px; }",
        ".article { margin-bottom: 20px; background: white; border-radius: 12px; padding: 16px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); transition: transform 0.15s ease, box-shadow 0.15s ease;}",
        ".title { font-size: 1.2em; font-weight: bold; }",
        ".summary { margin: 10px 0; color: #555; }",
        ".meta { color: #888; font-size: 0.9em; }",
        "a { color: #0066cc; text-decoration: none; }",
        "a:hover { text-decoration: underline; transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,0.12); }",
        "hr { border: none; border-top: 1px solid #ddd; margin: 20px 0; }",
        ".tabs { margin: 20px 0;}",
        ".tabs button { padding: 8px 16px; margin-right: 10px; border: none; background: #0066cc; color: white; border-radius: 6px; cursor: pointer; }",
        ".tabs button.active { background: #ff6600; color: white; }",
        ".tabs button:hover { background: #004c99;}",
        ".tab-content { display: none;}",
        "@media (prefers-color-scheme: dark) { body { background: #121212; color: #eee; } .article { background: #1e1e1e; } }",
        "</style>",
        "</head>",
        "<body>",
        "<h1>Tech Articles</h1>"
    ]
    html_parts.append("""
        <div class="tabs">
            <button onclick="showTab('HackerNews')">Hacker News</button>
            <button onclick="showTab('Hatena')">Hatena</button>
            <button onclick="showTab('Qiita')">Qiita</button>
        </div>
        """)
    
    # Hacker News セクション
    html_parts.append("<div id='HackerNews' class='tab-content'>")
    html_parts.append("<h2>Hacker News</h2>")
    if not hn_articles:
        html_parts.append("<p>No articles found.</p>")
    else:
        for article in hn_articles:
            title = article.get("title", "No Title")
            url = article.get("url", "#")
            summary = article.get("summary", article.get("excerpt", ""))
            points = article.get("points", 0)
            num_comments = article.get("num_comments", 0)
            
            html_parts.append("<div class='article'>")
            html_parts.append(f"<div class='title'><a href='{url}' target='_blank'>{title}</a></div>")
            html_parts.append(f"<div class='summary'>{summary}</div>")
            html_parts.append(f"<div class='meta'>Points: {points} | Comments: {num_comments}</div>")
            html_parts.append("</div>")
            html_parts.append("<hr>")
    html_parts.append("</div>")
    
    # はてなブックマーク セクション
    html_parts.append("<div id='Hatena' class='tab-content'>")
    html_parts.append("<h2>はてなブックマーク</h2>")
    if not hatena_articles:
        html_parts.append("<p>No articles found.</p>")
    else:
        for article in hatena_articles:
            title = article.get("title", "No Title")
            url = article.get("url", "#")
            summary = article.get("summary", article.get("excerpt", ""))
            points = article.get("points", 0)
            num_comments = article.get("num_comments", 0)
            
            html_parts.append("<div class='article'>")
            html_parts.append(f"<div class='title'><a href='{url}' target='_blank'>{title}</a></div>")
            html_parts.append(f"<div class='summary'>{summary}</div>")
            html_parts.append(f"<div class='meta'>Points: {points} | Comments: {num_comments}</div>")
            html_parts.append("</div>")
            html_parts.append("<hr>")
    html_parts.append("</div>")

    # Qiita セクション
    html_parts.append("<div id='Qiita' class='tab-content'>")
    html_parts.append("<h2>Qiita</h2>")
    if not qiita_articles:
        html_parts.append("<p>No articles found.</p>")
    else:
        for article in qiita_articles:
            title = article.get("title", "No Title")
            url = article.get("url", "#")
            summary = article.get("summary", article.get("excerpt", ""))
            points = article.get("points", 0)
            num_comments = article.get("num_comments", 0)
            
            html_parts.append("<div class='article'>")
            html_parts.append(f"<div class='title'><a href='{url}' target='_blank'>{title}</a></div>")
            html_parts.append(f"<div class='summary'>{summary}</div>")
            html_parts.append(f"<div class='meta'>Points: {points} | Comments: {num_comments}</div>")
            html_parts.append("</div>")
            html_parts.append("<hr>")
    html_parts.append("</div>")

    html_parts.append("</body>")
    html_parts.append("""
        <script>
            function showTab(id) {
                // 全コンテンツを非表示
                document.querySelectorAll(".tab-content").forEach(el => {
                    el.style.display = "none";
                });

                // 全ボタンからactive削除
                document.querySelectorAll(".tabs button").forEach(btn => {
                    btn.classList.remove("active");
                });

                // 対象コンテンツ表示
                document.getElementById(id).style.display = "block";

                // 押されたボタンをactive化
                event.target.classList.add("active");
            }

            // 初期表示
            document.addEventListener("DOMContentLoaded", function() {
                document.querySelector(".tabs button").classList.add("active");
                showTab("HackerNews");
            });
        </script>
        """)
    html_parts.append("</html>")
    
    return "\n".join(html_parts)


import os
import webbrowser
# from src.fetchers.hackernews import fetch_articles, normalize_articles
# from src.fetchers.hatena import fetch_articles, normalize_articles
from src.fetchers import hackernews, hatena, qiita
# from src.services.gemini_service import select_and_summarize
from src.services.gemini_service import select_by_source


def save_html(html_content: str) -> str:
    output_dir = os.path.join("src", "output")
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, "result.html")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return file_path


def open_in_browser(file_path: str) -> None:
    abs_path = os.path.abspath(file_path)
    webbrowser.open(f"file://{abs_path}")


def main() -> None:

    # ---------------------------
    # Step1: 各ソース取得
    # ---------------------------
    hn_raw = hackernews.fetch_articles()
    hatena_raw = hatena.fetch_articles()
    qiita_raw = qiita.fetch_articles()

    # ---------------------------
    # Step2: 正規化
    # ---------------------------
    hn_normalized = hackernews.normalize_articles(hn_raw)
    hatena_normalized = hatena.normalize_articles(hatena_raw)
    qiita_normalized = qiita.normalize_articles(qiita_raw)

    # ---------------------------
    # Step3: 全記事を結合
    # ---------------------------
    all_articles = (
        hn_normalized
        + hatena_normalized
        + qiita_normalized
    )

    # ---------------------------
    # Step4: 各source最大5件選定
    # ---------------------------
    selected = select_by_source(all_articles)

    # ---------------------------
    # Step5: source別に再分類
    # ---------------------------
    grouped: dict[str, list[dict]] = {}

    for article in selected:
        source = article.get("source", "Unknown")
        grouped.setdefault(source, []).append(article)

    # ---------------------------
    # Step6: HTML生成
    # ---------------------------
    html = generate_html(
        grouped.get("HackerNews", []),
        grouped.get("Hatena", []),
        grouped.get("Qiita", [])
    )

    # ---------------------------
    # Step7: 保存 & 表示
    # ---------------------------
    file_path = save_html(html)
    open_in_browser(file_path)


if __name__ == "__main__":
    main()
