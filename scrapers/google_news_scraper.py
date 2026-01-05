import feedparser
from urllib.parse import quote_plus


def fetch_google_news(keyword, max_results=10):
    # Clean + URL-encode the query (handles spaces and special chars)
    query = quote_plus(keyword.strip())
    feed_url = f"https://news.google.com/rss/search?q={query}"

    try:
        feed = feedparser.parse(feed_url)
    except Exception as e:
        print(f"[ERROR] Failed to fetch Google News feed: {e}")
        return []

    results = []

    # If parsing failed badly, feed.entries might be empty
    for entry in feed.entries[:max_results]:
        results.append(
            {
                "text": entry.title,
                "url": entry.link,
                "published": getattr(entry, "published", ""),
            }
        )

    return results
