import os
import webbrowser

from src.fetchers import hackernews, hatena, qiita
from src.services.gemini_service import select_by_source


def generate_html(hn_articles: list[dict], hatena_articles: list[dict], qiita_articles: list[dict]) -> str:
    import html

    def render_article_card(article: dict, source: str) -> list[str]:
        title = article.get("title", "No Title")
        url = article.get("url", "#")
        summary = article.get("summary", article.get("excerpt", ""))
        points = article.get("points", 0)
        num_comments = article.get("num_comments", 0)

        title_escaped = html.escape(str(title), quote=True)
        url_escaped = html.escape(str(url), quote=True)
        summary_escaped = html.escape(str(summary), quote=True)
        source_escaped = html.escape(str(source), quote=True)

        return [
            "<div class='article'>",
            f"<div class='title'><a href='{url_escaped}' target='_blank' rel='noopener noreferrer'>{title_escaped}</a></div>",
            f"<div class='summary'>{summary_escaped}</div>",
            f"<div class='meta'>Points: {points} | Comments: {num_comments}</div>",
            (
                f"<button class='read-later-btn' type='button' "
                f"data-title=\"{title_escaped}\" "
                f"data-url=\"{url_escaped}\" "
                f"data-summary=\"{summary_escaped}\" "
                f"data-source=\"{source_escaped}\">Read Later</button>"
            ),
            "</div>",
            "<hr>",
        ]

    html_parts = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "<meta charset='UTF-8'>",
        "<title>Tech Articles</title>",
        "<style>",
        "body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f7fa; color: #222; }",
        "h1 { color: #333; }",
        "h2 { color: #666; border-bottom: 2px solid #ddd; padding-bottom: 10px; margin-top: 24px; }",
        ".layout { display: flex; gap: 24px; align-items: flex-start; }",
        ".content-column { flex: 1 1 70%; min-width: 0; }",
        ".saved-column { flex: 0 0 340px; position: sticky; top: 20px; background: #fff; border-radius: 12px; padding: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }",
        ".saved-column h2 { margin-top: 0; }",
        ".saved-empty { color: #777; margin: 8px 0; }",
        ".saved-item { border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; margin-bottom: 12px; background: #fafcff; }",
        ".saved-item-title { font-size: 1em; font-weight: bold; margin-bottom: 6px; }",
        ".saved-item-summary { color: #555; margin: 8px 0; font-size: 0.95em; line-height: 1.4; }",
        ".saved-item-meta { color: #666; font-size: 0.85em; margin-bottom: 8px; }",
        ".saved-item-delete { border: none; background: #b91c1c; color: #fff; padding: 6px 10px; border-radius: 6px; cursor: pointer; }",
        ".saved-item-delete:hover { background: #991b1b; }",
        ".article { margin-bottom: 20px; background: white; border-radius: 12px; padding: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }",
        ".title { font-size: 1.2em; font-weight: bold; }",
        ".summary { margin: 10px 0; color: #555; }",
        ".meta { color: #888; font-size: 0.9em; }",
        ".read-later-btn { margin-top: 10px; border: none; background: #0f766e; color: #fff; padding: 8px 12px; border-radius: 6px; cursor: pointer; }",
        ".read-later-btn:hover { background: #0b5f59; }",
        "a { color: #0066cc; text-decoration: none; }",
        "a:hover { text-decoration: underline; }",
        "hr { border: none; border-top: 1px solid #ddd; margin: 20px 0; }",
        ".tabs { margin: 20px 0;}",
        ".tabs button { padding: 8px 16px; margin-right: 10px; border: none; background: #0066cc; color: white; border-radius: 6px; cursor: pointer; }",
        ".tabs button.active { background: #ff6600; color: white; }",
        ".tabs button:hover { background: #004c99;}",
        ".tab-content { display: none;}",
        "@media (max-width: 900px) { .layout { flex-direction: column; } .saved-column { position: static; width: 100%; } }",
        "@media (prefers-color-scheme: dark) { body { background: #121212; color: #eee; } .article, .saved-column { background: #1e1e1e; } .saved-item { background: #222; border-color: #333; } .saved-item-summary, .summary { color: #c7c7c7; } .saved-item-meta, .meta { color: #9ca3af; } }",
        "</style>",
        "</head>",
        "<body>",
        "<h1>Tech Articles</h1>",
        "<div class='layout'>",
        "<main class='content-column'>",
    ]

    html_parts.append("""
        <div class="tabs">
            <button data-tab="HackerNews" onclick="showTab('HackerNews', this)">Hacker News</button>
            <button data-tab="Hatena" onclick="showTab('Hatena', this)">Hatena</button>
            <button data-tab="Qiita" onclick="showTab('Qiita', this)">Qiita</button>
        </div>
        """)

    html_parts.append("<div id='HackerNews' class='tab-content'>")
    html_parts.append("<h2>Hacker News</h2>")
    if not hn_articles:
        html_parts.append("<p>No articles found.</p>")
    else:
        for article in hn_articles:
            html_parts.extend(render_article_card(article, "HackerNews"))
    html_parts.append("</div>")

    html_parts.append("<div id='Hatena' class='tab-content'>")
    html_parts.append("<h2>Hatena</h2>")
    if not hatena_articles:
        html_parts.append("<p>No articles found.</p>")
    else:
        for article in hatena_articles:
            html_parts.extend(render_article_card(article, "Hatena"))
    html_parts.append("</div>")

    html_parts.append("<div id='Qiita' class='tab-content'>")
    html_parts.append("<h2>Qiita</h2>")
    if not qiita_articles:
        html_parts.append("<p>No articles found.</p>")
    else:
        for article in qiita_articles:
            html_parts.extend(render_article_card(article, "Qiita"))
    html_parts.append("</div>")

    html_parts.extend([
        "</main>",
        "<aside class='saved-column'>",
        "<h2>Read Later</h2>",
        "<div id='savedArticlesList'></div>",
        "</aside>",
        "</div>",
        "</body>",
    ])

    html_parts.append("""
        <script>
            const STORAGE_KEY = "saved_articles";

            function showTab(id, button) {
                document.querySelectorAll(".tab-content").forEach(el => {
                    el.style.display = "none";
                });

                document.querySelectorAll(".tabs button").forEach(btn => {
                    btn.classList.remove("active");
                });

                document.getElementById(id).style.display = "block";

                if (button) {
                    button.classList.add("active");
                } else {
                    const matched = document.querySelector(`.tabs button[data-tab="${id}"]`);
                    if (matched) {
                        matched.classList.add("active");
                    }
                }
            }

            function loadSavedArticles() {
                try {
                    const savedRaw = localStorage.getItem(STORAGE_KEY);
                    if (!savedRaw) {
                        return [];
                    }
                    const parsed = JSON.parse(savedRaw);
                    return Array.isArray(parsed) ? parsed : [];
                } catch (error) {
                    console.error("Failed to parse saved articles", error);
                    return [];
                }
            }

            function saveArticle(article) {
                const savedArticles = loadSavedArticles();
                const exists = savedArticles.some(item => item.url === article.url);
                if (exists) {
                    return false;
                }

                savedArticles.unshift({
                    title: article.title,
                    url: article.url,
                    summary: article.summary,
                    source: article.source,
                    saved_at: new Date().toISOString()
                });
                localStorage.setItem(STORAGE_KEY, JSON.stringify(savedArticles));
                renderSavedArticles();
                return true;
            }

            function deleteArticle(url) {
                const savedArticles = loadSavedArticles();
                const updated = savedArticles.filter(item => item.url !== url);
                localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
                renderSavedArticles();
            }

            function formatSavedDate(savedAt) {
                const date = new Date(savedAt);
                if (Number.isNaN(date.getTime())) {
                    return savedAt;
                }
                return date.toLocaleString();
            }

            function renderSavedArticles() {
                const container = document.getElementById("savedArticlesList");
                const savedArticles = loadSavedArticles();
                container.innerHTML = "";

                if (savedArticles.length === 0) {
                    const empty = document.createElement("p");
                    empty.className = "saved-empty";
                    empty.textContent = "No saved articles yet.";
                    container.appendChild(empty);
                    return;
                }

                savedArticles.forEach(article => {
                    const item = document.createElement("div");
                    item.className = "saved-item";

                    const titleWrap = document.createElement("div");
                    titleWrap.className = "saved-item-title";
                    const link = document.createElement("a");
                    link.href = article.url;
                    link.target = "_blank";
                    link.rel = "noopener noreferrer";
                    link.textContent = article.title || "No Title";
                    titleWrap.appendChild(link);

                    const summary = document.createElement("div");
                    summary.className = "saved-item-summary";
                    summary.textContent = article.summary || "";

                    const meta = document.createElement("div");
                    meta.className = "saved-item-meta";
                    meta.textContent = `Source: ${article.source || "Unknown"} | Saved: ${formatSavedDate(article.saved_at)}`;

                    const removeBtn = document.createElement("button");
                    removeBtn.type = "button";
                    removeBtn.className = "saved-item-delete";
                    removeBtn.textContent = "Delete";
                    removeBtn.addEventListener("click", () => deleteArticle(article.url));

                    item.appendChild(titleWrap);
                    item.appendChild(summary);
                    item.appendChild(meta);
                    item.appendChild(removeBtn);
                    container.appendChild(item);
                });
            }

            function handleSaveClick(event) {
                const button = event.currentTarget;
                const article = {
                    title: button.dataset.title || "No Title",
                    url: button.dataset.url || "#",
                    summary: button.dataset.summary || "",
                    source: button.dataset.source || "Unknown"
                };

                const saved = saveArticle(article);
                if (!saved) {
                    button.textContent = "Already Saved";
                    setTimeout(() => {
                        button.textContent = "Read Later";
                    }, 1200);
                }
            }

            document.addEventListener("DOMContentLoaded", function() {
                document.querySelectorAll(".read-later-btn").forEach(button => {
                    button.addEventListener("click", handleSaveClick);
                });

                renderSavedArticles();

                const firstTabButton = document.querySelector(".tabs button[data-tab='HackerNews']");
                if (firstTabButton) {
                    showTab("HackerNews", firstTabButton);
                }
            });
        </script>
        """)
    html_parts.append("</html>")

    return "\n".join(html_parts)


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
    hn_raw = hackernews.fetch_articles()
    hatena_raw = hatena.fetch_articles()
    qiita_raw = qiita.fetch_articles()

    hn_normalized = hackernews.normalize_articles(hn_raw)
    hatena_normalized = hatena.normalize_articles(hatena_raw)
    qiita_normalized = qiita.normalize_articles(qiita_raw)

    all_articles = hn_normalized + hatena_normalized + qiita_normalized

    selected = select_by_source(all_articles)

    grouped: dict[str, list[dict]] = {}

    for article in selected:
        source = article.get("source", "Unknown")
        grouped.setdefault(source, []).append(article)

    html = generate_html(
        grouped.get("HackerNews", []),
        grouped.get("Hatena", []),
        grouped.get("Qiita", [])
    )

    file_path = save_html(html)
    open_in_browser(file_path)


if __name__ == "__main__":
    main()
