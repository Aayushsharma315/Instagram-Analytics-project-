"""
01_data_cleaning.py
------------------------------------------------
Cleans the raw Instagram export and produces an analysis-ready dataset.

Steps performed:
  1. Load raw CSV
  2. Drop exact duplicate rows
  3. Handle missing values (reach, comments, caption)
  4. Fix data types (datetime, integers)
  5. Feature engineering: engagement_rate, day_of_week, hour, month
  6. Export cleaned dataset to data/processed/

Run: python scripts/01_data_cleaning.py
"""

import pandas as pd
import numpy as np

RAW_PATH = "data/raw/instagram_posts_raw.csv"
OUT_PATH = "data/processed/instagram_posts_clean.csv"


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"Loaded {len(df)} rows, {df['post_id'].nunique()} unique post IDs")
    return df


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates(subset=["post_id"], keep="first")
    print(f"Removed {before - len(df)} duplicate rows")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    # Reach: impute with median of the same post_type (safer than global median)
    df["reach"] = df.groupby("post_type")["reach"].transform(
        lambda x: x.fillna(x.median())
    )
    # Comments: missing likely means 0 recorded comments at export time
    df["comments"] = df["comments"].fillna(0)
    # Caption: missing captions are valid (image-only posts) -> label explicitly
    df["caption"] = df["caption"].fillna("No caption")
    df["hashtags"] = df["hashtags"].fillna("")
    print("Missing values handled:")
    print(df.isna().sum()[df.isna().sum() > 0])
    return df


def fix_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    df["post_date"] = pd.to_datetime(df["post_date"])
    int_cols = ["reach", "impressions", "likes", "comments", "shares",
                "saves", "follows_gained", "hashtag_count"]
    for col in int_cols:
        df[col] = df[col].astype(int)
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df["total_engagement"] = df["likes"] + df["comments"] + df["shares"] + df["saves"]
    df["engagement_rate"] = (df["total_engagement"] / df["reach"]).round(4)
    df["day_of_week"] = df["post_date"].dt.day_name()
    df["hour"] = df["post_date"].dt.hour
    df["month"] = df["post_date"].dt.month_name()
    df["year"] = df["post_date"].dt.year

    # Simple time-of-day bucket, useful for posting-time analysis
    def bucket_hour(h):
        if 5 <= h < 12:
            return "Morning"
        elif 12 <= h < 17:
            return "Afternoon"
        elif 17 <= h < 21:
            return "Evening"
        return "Night"

    df["time_bucket"] = df["hour"].apply(bucket_hour)
    return df


def main():
    df = load_data(RAW_PATH)
    df = drop_duplicates(df)
    df = handle_missing_values(df)
    df = fix_dtypes(df)
    df = engineer_features(df)

    df.to_csv(OUT_PATH, index=False)
    print(f"\nCleaned dataset saved -> {OUT_PATH}")
    print(f"Final shape: {df.shape}")
    print(df.describe(include='all').T[["count", "mean", "std"]].head(10))


if __name__ == "__main__":
    main()
