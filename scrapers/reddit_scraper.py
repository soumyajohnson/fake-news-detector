import os
import praw
from dotenv import load_dotenv

load_dotenv()


def _get_reddit_client():
    """
    Initialize and return a read-only Reddit client.
    Returns None if credentials are missing or invalid.
    """
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")

    if not client_id or not client_secret or not user_agent:
        print("[ERROR] Reddit credentials missing. "
              "Check REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT in .env")
        return None

    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )
        reddit.read_only = True
        return reddit
    except Exception as e:
        print(f"[ERROR] Failed to initialize Reddit client: {e}")
        return None


def fetch_reddit_posts(keyword, subreddit="news", limit=10):
    """
    Fetch posts from Reddit matching the keyword.
    Returns a list of dicts: { 'text': title, 'url': url }.
    On any error, returns [] and logs what happened.
    """
    reddit = _get_reddit_client()
    if reddit is None:
        # Credentials / client issue
        return []

    try:
        posts = reddit.subreddit(subreddit).search(
            keyword, sort="new", limit=limit
        )
        return [{"text": post.title, "url": post.url} for post in posts]
    except Exception as e:
        print(f"[ERROR] Reddit API error while searching '{keyword}': {e}")
        return []
