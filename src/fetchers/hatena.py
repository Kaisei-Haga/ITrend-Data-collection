import feedparser

def fetch_articles() -> list[dict]:
    url = "https://b.hatena.ne.jp/hotentry/it.rss"
    
    feed = feedparser.parse(url)
    
    if feed.bozo:  # パースエラーがあった場合
        raise Exception(f"RSS feed parsing failed: {feed.bozo_exception}")
    
    entries = feed.entries
    
    return entries[:30]


def normalize_articles(articles: list[dict]) -> list[dict]:
    normalized = []
    
    for article in articles:
        url = article.get("link", "")
        title = article.get("title", "")
        
        if not url or not title:
            continue
        
        # RSSフィードから説明文を取得
        excerpt = article.get("summary", "") or article.get("description", "")
        
        # はてなブックマークのRSSには、dc:subjectにブックマーク数が含まれることがある
        # ただし、標準的なRSSフィードには含まれないため、0または抽出ロジックが必要
        points = 0  # ブックマーク数（RSSからは直接取得できない）
        num_comments = 0  # コメント数（RSSからは直接取得できない）
        
        normalized.append({
            "title": title,
            "url": url,
            "excerpt": excerpt,
            "points": points,
            "num_comments": num_comments,
            "source": "Hatena"
        })
    
    return normalized
