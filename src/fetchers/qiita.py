import requests
from datetime import datetime, timedelta


def fetch_articles() -> list[dict]:
    seven_days_ago = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    url = "https://qiita.com/api/v2/items"
    params = {
        "query": f"created:>{seven_days_ago} stocks:>20",
        "per_page": 30
    }
    
    response = requests.get(url, params=params, timeout=10)
    
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")
    
    data = response.json()
    
    return data


def normalize_articles(raw: list[dict]) -> list[dict]:
    normalized = []
    
    for article in raw:
        url = article.get("url", "")
        title = article.get("title", "")
        
        if not url or not title:
            continue
        
        body = article.get("body", "")
        excerpt = body[:300] if body else ""
        points = article.get("likes_count", 0)
        num_comments = article.get("comments_count", 0)
        
        normalized.append({
            "title": title,
            "url": url,
            "excerpt": excerpt,
            "points": points,
            "num_comments": num_comments,
            "source": "Qiita"
        })
    
    return normalized
