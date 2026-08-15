"""
00_generate_dataset.py
------------------------------------------------
Generates a realistic synthetic Instagram post-performance dataset.

Why synthetic data?
Instagram's official API restricts bulk historical data pulls, and public
Kaggle dumps are often outdated or inconsistently labeled. For this project
a synthetic-but-realistic dataset was generated using controlled statistical
distributions (informed by publicly reported industry engagement benchmarks)
so the analysis pipeline (cleaning -> EDA -> SQL -> BI dashboards) can be
demonstrated end-to-end on a clean, reproducible dataset.

Output: data/raw/instagram_posts_raw.csv
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

N_POSTS = 620

post_types = ["Reel", "Carousel", "Image", "Video"]
post_type_weights = [0.42, 0.28, 0.22, 0.08]

# Base engagement multipliers per post type (Reels typically outperform)
engagement_multiplier = {"Reel": 1.6, "Carousel": 1.25, "Image": 1.0, "Video": 1.1}

hashtag_pool = [
    "#fashion", "#travel", "#foodie", "#fitness", "#lifestyle", "#photography",
    "#reels", "#explorepage", "#motivation", "#ootd", "#nature", "#art",
    "#business", "#startup", "#technology", "#marketing", "#india", "#delhi",
    "#mumbai", "#instagood"
]

captions_templates = [
    "Check out our latest {topic} update! What do you think?",
    "Behind the scenes of {topic} — swipe to see more.",
    "5 tips every beginner should know about {topic}.",
    "We just launched something new in {topic}. Link in bio!",
    "A day in the life: {topic} edition.",
    "Big announcement coming soon about {topic}!",
    "Why {topic} matters more than you think.",
    "",  # some posts have no caption
]

topics = ["fashion", "fitness", "food", "travel", "tech", "business", "art", "wellness"]

start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
date_range_days = (end_date - start_date).days

rows = []
for post_id in range(1, N_POSTS + 1):
    ptype = np.random.choice(post_types, p=post_type_weights)
    post_date = start_date + timedelta(days=random.randint(0, date_range_days),
                                        hours=random.randint(0, 23),
                                        minutes=random.randint(0, 59))

    # Base reach depends on post type + some randomness (log-normal for realism)
    base_reach = np.random.lognormal(mean=8.2, sigma=0.55) * engagement_multiplier[ptype]
    reach = int(max(150, base_reach))

    # Impressions are always >= reach
    impressions = int(reach * np.random.uniform(1.1, 1.6))

    # Engagement rate varies by post type, with noise
    base_er = {"Reel": 0.065, "Carousel": 0.048, "Image": 0.035, "Video": 0.04}[ptype]
    engagement_rate = max(0.005, np.random.normal(base_er, 0.015))

    likes = int(reach * engagement_rate * np.random.uniform(0.75, 0.95))
    comments = int(likes * np.random.uniform(0.01, 0.06))
    shares = int(reach * np.random.uniform(0.002, 0.02) * engagement_multiplier[ptype])
    saves = int(reach * np.random.uniform(0.003, 0.03) * engagement_multiplier[ptype])

    n_hashtags = random.randint(0, 8)
    hashtags = " ".join(random.sample(hashtag_pool, n_hashtags)) if n_hashtags else ""

    topic = random.choice(topics)
    caption = random.choice(captions_templates).format(topic=topic)

    follows_gained = int(saves * np.random.uniform(0.05, 0.25))

    # Inject some realistic messiness for the cleaning phase
    if random.random() < 0.03:
        comments = np.nan
    if random.random() < 0.02:
        caption = None
    if random.random() < 0.015:
        reach = None

    rows.append({
        "post_id": f"IG{post_id:04d}",
        "post_date": post_date.strftime("%Y-%m-%d %H:%M:%S"),
        "post_type": ptype,
        "caption": caption,
        "hashtags": hashtags,
        "hashtag_count": n_hashtags,
        "reach": reach,
        "impressions": impressions,
        "likes": likes,
        "comments": comments,
        "shares": shares,
        "saves": saves,
        "follows_gained": follows_gained,
    })

df = pd.DataFrame(rows)

# Introduce a handful of exact duplicate rows (common real-world data issue)
dupes = df.sample(6, random_state=1)
df = pd.concat([df, dupes], ignore_index=True)

df.to_csv("data/raw/instagram_posts_raw.csv", index=False)
print(f"Generated {len(df)} rows -> data/raw/instagram_posts_raw.csv")
print(df.head())
