from model.predict import predict_news
from scrapers.twitter_scraper import fetch_tweets
from scrapers.reddit_scraper import fetch_reddit_posts
from scrapers.google_news_scraper import fetch_google_news
from keybert import KeyBERT

# === Load keyword extractor ===
kw_model = KeyBERT()

def build_search_term(text: str) -> str:
    words = text.split()
    if len(words) <= 12:
        return text

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

def display_posts(posts, source):
    if not posts:
        print(f"[{source.upper()}] No posts found.\n")
        return
    for post in posts:
        print(f"[{source.upper()}] {post['text']}\n→ {post.get('url', '')}\n")


# === Step 1: User input ===
user_input = input("📰 Paste the news headline or article:\n>> ")

# === Step 2: Run prediction with confidence ===
label, confidence, probs = predict_news(user_input)

print(f"\n🔍 Prediction: {label.upper()}")
print(f"📊 Confidence: {confidence*100:.2f}%")
print(f"    → Probabilities: FAKE={probs[0]:.4f}, REAL={probs[1]:.4f}")


# === Step 3: If prediction is FAKE → stop here ===
if label.upper() == "FAKE":
    print("\n⚠️ No context will be fetched because the news appears to be FAKE.")
    exit(0)

# === Step 4: Extract keywords ===
search_term = build_search_term(user_input)
print(f"\n🔑 Keywords used for context: {search_term}")

# === Step 5: Fetch REAL context ===
print("\n📡 Fetching related Twitter posts...")
twitter_posts = fetch_tweets(search_term, max_results=5)

print("\n📡 Fetching related Reddit posts...")
reddit_posts = fetch_reddit_posts(search_term, limit=5)

print("\n📡 Fetching related Google News headlines...")
google_posts = fetch_google_news(search_term, max_results=5)

# === Step 6: Display results ===
print("\n🧠 SOCIAL CONTEXT (shown only for REAL predictions)\n------------------------------------------------")
# display_posts(twitter_posts, "twitter")
display_posts(reddit_posts, "reddit")
display_posts(google_posts, "google")
