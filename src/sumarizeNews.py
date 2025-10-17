from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_article(title, content):
    prompt = f"Summarize this African startup news article in 300 words:\n\nTitle: {title}\n\nContent: {content}"
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content.strip()
