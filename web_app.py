from flask import Flask, render_template, request
from keybert import KeyBERT

from model.predict import predict_news
from scrapers.twitter_scraper import fetch_tweets
from scrapers.reddit_scraper import fetch_reddit_posts
from scrapers.google_news_scraper import fetch_google_news

app = Flask(__name__)
kw_model = KeyBERT()


def build_search_term(text: str) -> str:
    """Build a good search term from the user input."""
    words = text.split()

    # For short headlines, just use the full text
    if len(words) <= 12:
        return text

    # For longer text, use KeyBERT to extract keyphrases
    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2),
        stop_words="english",
        top_n=3,
    )
    keyphrases = [kw for kw, _ in keywords if len(kw.split()) > 1]
    if not keyphrases:
        keyphrases = [kw for kw, _ in keywords]

    return " ".join(keyphrases)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    context = {"twitter": [], "reddit": [], "google": []}

    if request.method == "POST":
        headline = request.form.get("headline", "").strip()

        if headline:
            # IMPORTANT: predict_news should return (label, confidence, probs)
            label, confidence, probs = predict_news(headline)

            result = {
                "headline": headline,
                "label": label.upper(),
                "confidence": round(confidence * 100, 2),
                "probs": {
                    "fake": round(probs[0] * 100, 2),
                    "real": round(probs[1] * 100, 2),
                },
            }

            # Only fetch context if model predicts REAL
            if label.upper() == "REAL":
                search_term = build_search_term(headline)

                twitter_posts = fetch_tweets(search_term, max_results=5)
                reddit_posts = fetch_reddit_posts(search_term, limit=5)
                google_posts = fetch_google_news(search_term, max_results=5)

                context = {
                    "search_term": search_term,
                    "twitter": twitter_posts,
                    "reddit": reddit_posts,
                    "google": google_posts,
                }

    return render_template("index.html", result=result, context=context)


if __name__ == "__main__":
    # Run with: python web_app.py
    app.run(debug=True)
