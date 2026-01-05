import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")  # folder that contains the 4 CSVs


def load_split(filename: str, label: str, source: str) -> pd.DataFrame:
    """Load one CSV and add label + source columns."""
    path = DATA_DIR / filename
    df = pd.read_csv(path)
    df["label"] = label          # "FAKE" or "REAL"
    df["source"] = source        # "gossipcop" or "politifact"

    # tweet_ids is one string with IDs separated by spaces/tabs
    # convert to number of tweets for basic analysis
    df["num_tweets"] = (
        df["tweet_ids"]
        .fillna("")
        .astype(str)
        .apply(lambda x: len(str(x).split()))
    )

    # length of title
    df["title_char_len"] = df["title"].astype(str).str.len()
    df["title_word_len"] = df["title"].astype(str).str.split().str.len()

    return df


def main():
    # 1. Load all four datasets
    gc_fake  = load_split("gossipcop_fake.csv",  "FAKE", "gossipcop")
    gc_real  = load_split("gossipcop_real.csv",  "REAL", "gossipcop")
    pf_fake  = load_split("politifact_fake.csv", "FAKE", "politifact")
    pf_real  = load_split("politifact_real.csv", "REAL", "politifact")

    # 2. Combine
    df = pd.concat([gc_fake, gc_real, pf_fake, pf_real], ignore_index=True)

    print("=== BASIC INFO ===")
    print("Shape:", df.shape)
    print("Columns:", list(df.columns))
    print()

    # 3. Counts by file / label / source
    print("=== COUNTS BY LABEL ===")
    print(df["label"].value_counts())
    print("\n=== COUNTS BY SOURCE ===")
    print(df["source"].value_counts())
    print("\n=== COUNTS BY SOURCE + LABEL ===")
    print(df.groupby(["source", "label"])["id"].count())
    print()

    # 4. Missing values
    print("=== MISSING VALUES (fraction) ===")
    print(df.isna().mean())
    print()

    # 5. Title length stats
    print("=== TITLE LENGTH (CHARS) BY LABEL ===")
    print(df.groupby("label")["title_char_len"].describe())
    print("\n=== TITLE LENGTH (WORDS) BY LABEL ===")
    print(df.groupby("label")["title_word_len"].describe())
    print()

    # 6. Tweet count stats
    print("=== NUMBER OF TWEETS PER ARTICLE (num_tweets) BY SOURCE ===")
    print(df.groupby("source")["num_tweets"].describe())
    print("\n=== NUMBER OF TWEETS PER ARTICLE BY LABEL ===")
    print(df.groupby("label")["num_tweets"].describe())
    print()

    # 7. Check duplicates (same url or same title)
    print("=== POSSIBLE DUPLICATES BY news_url ===")
    dup_urls = df[df.duplicated("news_url", keep=False)].sort_values("news_url")
    print(dup_urls[["news_url", "source", "label"]].head(10))
    print()

    print("=== POSSIBLE DUPLICATES BY title ===")
    dup_titles = df[df.duplicated("title", keep=False)].sort_values("title")
    print(dup_titles[["title", "source", "label"]].head(10))
    print()

    # 8. Show example rows
    print("=== EXAMPLE FAKE NEWS TITLES ===")
    print(df[df["label"] == "FAKE"][["title", "source", "num_tweets"]].head(5))
    print("\n=== EXAMPLE REAL NEWS TITLES ===")
    print(df[df["label"] == "REAL"][["title", "source", "num_tweets"]].head(5))


if __name__ == "__main__":
    main()
