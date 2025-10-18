import os
from openai import OpenAI

#loading the API keys for Git, local and stramlit
try:
    import streamlit as st
    api_key = st.secrets.get("OPENAI_API_KEY", None)
except Exception:
    api_key = None

if not api_key:
    api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Missing OPENAI_API_KEY. Please set it in Streamlit Secrets or as an environment variable.")

client = OpenAI(api_key=api_key)


def summarize_article(title, content):
    prompt = f"Summarize this African startup news article in 300 words:\n\nTitle: {title}\n\nContent: {content}"
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content.strip()
