def filter_africa_stories(articles, limit=10):
    keywords = ["africa", "nigeria", "kenya", "ghana", "south africa", "startup", "funding", "fintech", "investment"]
    filtered = []
    for article in articles:
        title = (article.get("title") or "").lower()
        description = (article.get("description") or "").lower()
        combined = f"{title} {description}"
        if any(k in combined for k in keywords):
            filtered.append(article)
    print(f"Filtered {len(filtered)} stories") 
    return filtered[:limit]
