import os
import requests
import json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
SAMPLE_FILE = os.path.join(DATA_DIR, "afriNews.json")


def fetch_africa_news():
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q=africa+startup+funding&language=en&sortBy=publishedAt&pageSize=50&apiKey={NEWS_API_KEY}"
    )
    
    try:
        response = requests.get(url)
        data = response.json()
        print("Response status:", data.get("status", "unknown"))

        # If API call successful
        if data.get("status") == "ok":
            articles = data.get("articles", [])
            print(f"Successfully fetched {len(articles)} articles.")

            # Save backup file for offline use
            with open(SAMPLE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
                print("Saved a local copy of fetched news.")
            return articles

        # If error (rate limit, bad key, etc.)
        else:
            print(f"API Error: {data.get('message', 'Unknown error')}")
            if os.path.exists(SAMPLE_FILE):
                print("Loading from local backup file...")
                with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                    return cached.get("articles", [])
            else:
                print("No local backup found.")
                return []

    except Exception as e:
        print(f"Exception occurred: {e}")
        return []
