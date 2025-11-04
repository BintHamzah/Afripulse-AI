import os
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# This file handles external API calls and basic data cleaning

NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

def clean_text(text):
    """Removes HTML tags from text."""
    if not text:
        return ""
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text().strip()


def fetch_news_api():
    """Fetches relevant news headlines from NewsAPI, focusing on business/tech."""
    if not NEWS_API_KEY:
        # This print statement will only show if the environment variable is not set
        print("NEWS_API_KEY not set.") 
        return []

    print("Fetching news from NewsAPI...")
    q_query = "startup OR 'venture capital' OR 'funding' OR business technology"
    
    # Fetch articles from the last 7 days
    from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    params = {
        'q': q_query,
        'language': 'en',
        'sortBy': 'publishedAt',
        'from': from_date,
        'pageSize': 100, 
        'apiKey': NEWS_API_KEY
    }
    
    try:
        response = requests.get('https://newsapi.org/v2/everything', params=params, timeout=15)
        response.raise_for_status() 
        data = response.json()
        print(f"NewsAPI returned {len(data.get('articles', []))} articles.")
        return data.get('articles', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching NewsAPI data: {e}")
        return []
