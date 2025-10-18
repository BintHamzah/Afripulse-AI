import datetime
from pathlib import Path

def generate_weekly_digest(summaries):
    
    today = datetime.date.today().strftime("%B %d, %Y")
    md_content = f"# Today's Digest – {today}\n\n"

    for i, story in enumerate(summaries, 1):
        md_content += f"### {i}. [{story['title']}]({story['url']})\n{story['summary']}\n\n"

    return summaries, md_content

