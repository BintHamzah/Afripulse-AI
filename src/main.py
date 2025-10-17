import os
from dotenv import load_dotenv
from pathlib import Path

from src.fetchNews import fetch_africa_news
from src.filterNews import filter_africa_stories
from src.sumarizeNews import summarize_article
from src.generateDigest import generate_weekly_digest

# Load .env
cwd = Path().resolve()
env_path = cwd / ".env"
if not env_path.exists():
    env_path = cwd.parent / ".env"
load_dotenv(dotenv_path=env_path)

print("Fetching latest Africa startup news...")
news = fetch_africa_news()
print(f"Fetched {len(news)} articles")

filtered_news = filter_africa_stories(news)
print(f"Filtered to {len(filtered_news)} Africa-related stories")

summaries = []
for item in filtered_news[:10]:
    summary = summarize_article(item["title"], item.get("description", ""))
    summaries.append({
        "title": item["title"],
        "url": item["url"],
        "summary": summary
    })

generate_weekly_digest(summaries)

# print("\n Top Summaries:")
# for i, s in enumerate(summaries, 1):
#     print(f"\n{i}. {s['title']}\n{s['summary']}\n{s['url']}")
