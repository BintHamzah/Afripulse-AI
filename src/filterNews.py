from datetime import datetime

# Filtering keywords and regions
AFRICAN_COUNTRIES = [
    "Nigeria", "Kenya", "South Africa", "Egypt", "Ghana", "Morocco", "Tunisia",
    "Senegal", "Rwanda", "Uganda", "Tanzania", "Ethiopia", "Africa" 
]
KEYWORDS = ["startup", "funding", "investment", "venture capital", "VC", "seed round", "fintech", "agritech"]


def filter_africa_stories(articles):
    """Filters articles to include only Africa-focused startup/VC stories."""
    print("Filtering articles for Africa-specific content...")
    filtered_stories = []
    # Combine lists for scoring
    filter_terms = AFRICAN_COUNTRIES + KEYWORDS
    
    for article in articles:
        # Check title and description for keywords
        text_to_check = (article.get('title', '') + " " + article.get('description', '')).lower()

        country_match = any(country.lower() in text_to_check for country in AFRICAN_COUNTRIES)
        keyword_match = any(keyword.lower() in text_to_check for keyword in KEYWORDS)
        
        if country_match and keyword_match:
            # Calculate a simple relevance score
            relevance_score = sum(text_to_check.count(term.lower()) for term in filter_terms)
            article['relevance_score'] = relevance_score
            filtered_stories.append(article)

    print(f"Filtered down to {len(filtered_stories)} relevant stories.")
    return filtered_stories

def rank_and_select_top_stories(stories, top_n=10):
    """Ranks stories by relevance (score) and recency, then selects the top N."""
    
    for story in stories:
        try:
            # Convert published date string to datetime object for sorting
            story['published_dt'] = datetime.fromisoformat(story['publishedAt'].replace('Z', '+00:00'))
        except (TypeError, ValueError):
            story['published_dt'] = datetime.min # Use minimum date for stories with invalid dates

    # Sort primarily by relevance score (high to low) and secondarily by date (most recent first)
    sorted_stories = sorted(
        stories,
        key=lambda x: (x.get('relevance_score', 0), x.get('published_dt', datetime.min)),
        reverse=True
    )
    
    print(f"Ranked and selected top {min(len(sorted_stories), top_n)} stories.")
    return sorted_stories[:top_n]
