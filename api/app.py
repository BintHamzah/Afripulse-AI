import os
from datetime import datetime

# === Imports from Modular Files ===
from summarizeNews import summarize_article
from fetchNews import fetch_news_api, clean_text
from filterNews import filter_africa_stories, rank_and_select_top_stories
# === Firestore Imports for Cloud Environment ===
import firebase_admin
from firebase_admin import firestore
# ===============================================

# --- CONFIGURATION (READ FROM OS ENVIRONMENT) ---
# Global keys will be set by the GCF entry point (generate_digest_http.py)
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def save_to_firestore(top_stories):
    """Saves the weekly digest to a public Firestore collection."""
    print("Attempting to save digest to Firestore...")
    today_date = datetime.now().strftime('%Y-%m-%d')
    APP_ID = "afripulse-ai-digest" 
    
    # Define collection and document paths
    COLLECTION_PATH = f"artifacts/{APP_ID}/public/data/digests" 
    DOCUMENT_ID = f"digest-{today_date}"

    digest_data = {
        "published_date": today_date,
        "timestamp": datetime.now().isoformat(),
        "top_stories": []
    }
    
    for i, story in enumerate(top_stories, 1):
        story_data = {
            "rank": i,
            "title": story.get('title', 'Untitled'),
            "summary": story.get('summary', 'Summary not available.'),
            "source": story.get('source', {}).get('name', 'N/A'),
            "url": story.get('url', '#'),
            "published_at": story.get('publishedAt', 'N/A'),
        }
        digest_data["top_stories"].append(story_data)
         
    # --- FIREBASE ADMIN SDK WRITE ---
    try:
        if not firebase_admin._apps:
             print("Initializing Firebase Admin SDK...")
             # Initializes using the service account credentials provided by GCF environment
             firebase_admin.initialize_app() 
        
        db = firestore.client()
        
        # 1. Write the new document with the date-specific ID
        doc_ref = db.collection(COLLECTION_PATH).document(DOCUMENT_ID)
        doc_ref.set(digest_data)
        print(f"Digest saved successfully to Firestore: {COLLECTION_PATH}/{DOCUMENT_ID}")
        
        # 2. Update the 'latest' pointer document for easy frontend fetching
        latest_doc_ref = db.collection(COLLECTION_PATH).document('latest')
        latest_doc_ref.set({"latest_digest_id": DOCUMENT_ID, "timestamp": datetime.now()})
        print("Updated 'latest' pointer.")
        
        return {"published_date": today_date, "status": "Success", "digest_data": digest_data}

    except Exception as e:
        print(f"Error saving to Firestore: {e}")
        return {"published_date": today_date, "status": f"Firestore write failed: {e}", "digest_data": digest_data}


def run_digest_generation():
    print("--- Running run_digest_generation ---")
    """
    Orchestrates the entire weekly digest generation process by calling 
    functions from the dedicated modules.
    """
    if not NEWS_API_KEY or not GEMINI_API_KEY:
        print("\n--- CRITICAL ERROR ---\nAPI keys are missing.")
        return {"error": "API keys are not configured."}
        
    # [1] Fetch News 
    all_articles = fetch_news_api()
    
    if not all_articles:
        # If no articles fetched, log and return error status
        return {"error": "No articles fetched."}

    # [2] Filter Stories
    # relevant_stories = filter_africa_stories(all_articles)
    
    # if not relevant_stories:
    #     # Save an empty digest to update the 'latest' pointer even if no stories found
    #     return save_to_firestore([]) 

    # print("Starting AI summarization (This may take a moment)...")
    # for story in relevant_stories:
    #     # [3] Clean and Summarize
    #     story['description'] = clean_text(story.get('description', ''))
    #     story['summary'] = summarize_article(story, GEMINI_API_KEY)
    #     print(f"    Summary complete for: {story.get('title', 'Unknown Title')[:50]}...")

    # [4] Select Top 10
    # top_10_stories = rank_and_select_top_stories(relevant_stories)

    # [5] Save the final content to Firestore
    # return save_to_firestore(top_10_stories)
