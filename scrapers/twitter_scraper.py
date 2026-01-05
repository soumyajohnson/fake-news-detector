import subprocess
import json

def fetch_tweets(keyword, max_results=10):
    command = f"snscrape --jsonl --max-results {max_results} twitter-search \"{keyword}\""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    tweets = []
    for line in result.stdout.splitlines():
        tweet = json.loads(line)
        tweets.append({
            "text": tweet.get("content", ""),
            "url": tweet.get("url", ""),
            "date": tweet.get("date", "")
        })
    return tweets
