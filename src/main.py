from src.fetchNews import fetch_africa_news
from src.filterNews import filter_africa_stories
from src.sumarizeNews import summarize_article
from src.generateDigest import generate_weekly_digest

news = fetch_africa_news()
filtered_news = filter_africa_stories(news)

# --- summarize top 10 ---
summaries = []
for item in filtered_news[:10]:
    summary = summarize_article(item["title"], item.get("description", ""))
    summaries.append({
        "title": item["title"],
        "url": item["url"],
        "summary": summary
    })

# --- generate array & markdown ---
summaries_array, digest_md = generate_weekly_digest(summaries)