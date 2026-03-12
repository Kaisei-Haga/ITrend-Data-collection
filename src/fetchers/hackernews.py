import requests
import time


def fetch_articles() -> list[dict]:
    seven_days_ago = int(time.time()) - (7 * 24 * 60 * 60)
    
    url = "https://hn.algolia.com/api/v1/search_by_date"
    params = {
        "tags": "story",
        "numericFilters": f"created_at_i>{seven_days_ago},points>80,num_comments>20"
    }
    
    response = requests.get(url, params=params, timeout=10)
    
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")
    
    data = response.json()
    hits = data.get("hits", [])
    
    return hits[:30]


def normalize_articles(articles: list[dict]) -> list[dict]:
    normalized = []
    
    for article in articles:
        url = article.get("url", "")
        title = article.get("title", "")
        
        if not url or not title:
            continue
        
        excerpt = article.get("story_text", "") or article.get("comment_text", "") or ""
        points = article.get("points", 0)
        num_comments = article.get("num_comments", 0)
        
        normalized.append({
            "title": title,
            "url": url,
            "excerpt": excerpt,
            "points": points,
            "num_comments": num_comments,
            "source": "HackerNews"
        })
    
    return normalized
