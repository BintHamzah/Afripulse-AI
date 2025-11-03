import requests
import json
import time

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent"
MODEL_NAME = "gemini-2.5-flash-preview-09-2025"

def summarize_article(article_data, gemini_api_key, retries=3):
    """
    Uses the Gemini API to summarize the article content.
    Accepts the article data and the API key.
    """
    if not gemini_api_key:
        return "Summary generation failed: GEMINI_API_KEY not provided."
        
    title = article_data.get('title', 'Untitled')
    source = article_data.get('source', {}).get('name', 'Unknown Source')
    description = article_data.get('description', '')
    
    system_prompt = (
        "You are an expert financial news analyst focused on the African tech and venture capital space. "
        "Your task is to summarize the provided news article into exactly 3 to 5 concise, high-impact sentences. "
        "The summary must be professional, informative, and suitable for a weekly executive digest."
    )
    
    user_query = (
        f"Summarize the following article for an executive weekly digest. "
        f"Title: {title}. "
        f"Source: {source}. "
        f"Abstract/Description: {description}"
    )

    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
    }
    
    for attempt in range(retries):
        try:
            response = requests.post(
                f"{GEMINI_API_URL}?key={gemini_api_key}",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(payload),
                timeout=20
            )
            response.raise_for_status()
            
            result = response.json()
            text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '').strip()
            
            if text:
                return text
            
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                print(f"API call failed (Attempt {attempt + 1}). Retrying...")
                time.sleep(2 * (2 ** attempt))
            else:
                print(f"Failed to summarize story after {retries} attempts: {e}")
                break
        except Exception as e:
            print(f"An unexpected error occurred during summarization: {e}")
            break
        
    return "Summary generation failed or returned empty content."
