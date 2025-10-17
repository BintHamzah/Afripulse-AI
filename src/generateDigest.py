import datetime
from pathlib import Path

def generate_weekly_digest(summaries):
    today = datetime.date.today().strftime("%B %d, %Y")
    md_content = f"# Today's Digest – {today}\n\n"

    for i, story in enumerate(summaries, 1):
        md_content += f"### {i}. [{story['title']}]({story['url']})\n{story['summary']}\n\n"

    output_dir = Path(__file__).resolve().parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "weeklyDigest.md"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"Weekly digest saved to {output_path}")
