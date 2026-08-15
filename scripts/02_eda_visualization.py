"""
02_eda_visualization.py
------------------------------------------------
Exploratory Data Analysis on the cleaned Instagram dataset.
Generates all charts used in the README / Power BI & Tableau prep.

Business questions answered:
  Q1. Which post type drives the highest engagement rate?
  Q2. What is the best day/time to post?
  Q3. Does hashtag count correlate with reach?
  Q4. How has engagement trended month over month?
  Q5. Which posts are top/bottom performers?

Run: python scripts/02_eda_visualization.py
Outputs: visuals/*.png
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["figure.dpi"] = 120

df = pd.read_csv("data/processed/instagram_posts_clean.csv", parse_dates=["post_date"])

# ---------------------------------------------------------------
# Q1: Engagement rate by post type
# ---------------------------------------------------------------
plt.figure(figsize=(7, 5))
order = df.groupby("post_type")["engagement_rate"].mean().sort_values(ascending=False).index
sns.barplot(data=df, x="post_type", y="engagement_rate", order=order,
            color="steelblue", errorbar=None)
plt.title("Average Engagement Rate by Post Type")
plt.ylabel("Engagement Rate")
plt.xlabel("Post Type")
plt.tight_layout()
plt.savefig("visuals/01_engagement_by_posttype.png")
plt.close()

# ---------------------------------------------------------------
# Q2: Best day & time to post (heatmap)
# ---------------------------------------------------------------
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
pivot = df.pivot_table(values="engagement_rate", index="day_of_week",
                        columns="time_bucket", aggfunc="mean").reindex(day_order)
pivot = pivot[["Morning", "Afternoon", "Evening", "Night"]]

plt.figure(figsize=(8, 5.5))
sns.heatmap(pivot, annot=True, fmt=".3f", cmap="YlOrRd", cbar_kws={"label": "Avg Engagement Rate"})
plt.title("Best Day & Time to Post (Avg Engagement Rate)")
plt.ylabel("")
plt.xlabel("")
plt.tight_layout()
plt.savefig("visuals/02_best_time_heatmap.png")
plt.close()

# ---------------------------------------------------------------
# Q3: Hashtag count vs reach
# ---------------------------------------------------------------
plt.figure(figsize=(7, 5))
sns.regplot(data=df, x="hashtag_count", y="reach", scatter_kws={"alpha": 0.35},
            line_kws={"color": "red"})
plt.title("Hashtag Count vs Reach")
plt.xlabel("Number of Hashtags Used")
plt.ylabel("Reach")
plt.tight_layout()
plt.savefig("visuals/03_hashtags_vs_reach.png")
plt.close()

corr = df[["hashtag_count", "reach"]].corr().iloc[0, 1]
print(f"Correlation (hashtag_count vs reach): {corr:.3f}")

# ---------------------------------------------------------------
# Q4: Monthly engagement trend
# ---------------------------------------------------------------
monthly = df.set_index("post_date").resample("ME")["total_engagement"].sum()

plt.figure(figsize=(9, 5))
monthly.plot(marker="o", color="#8b3ff5")
plt.title("Monthly Total Engagement Trend")
plt.ylabel("Total Engagement")
plt.xlabel("Month")
plt.tight_layout()
plt.savefig("visuals/04_monthly_engagement_trend.png")
plt.close()

# ---------------------------------------------------------------
# Q5: Top 10 performing posts
# ---------------------------------------------------------------
top10 = df.nlargest(10, "engagement_rate")[["post_id", "post_type", "engagement_rate", "reach"]]

plt.figure(figsize=(8, 5.5))
sns.barplot(data=top10, x="engagement_rate", y="post_id", hue="post_type", dodge=False, palette="mako")
plt.title("Top 10 Posts by Engagement Rate")
plt.xlabel("Engagement Rate")
plt.ylabel("Post ID")
plt.tight_layout()
plt.savefig("visuals/05_top10_posts.png")
plt.close()

print("\nAll charts saved to visuals/")
print("\nSummary stats by post type:")
print(df.groupby("post_type")["engagement_rate"].agg(["mean", "count"]).sort_values("mean", ascending=False))
