import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(
    page_title="Instagram Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "processed" / "instagram_posts_clean.csv"

df = pd.read_csv(DATA_FILE)

df["post_date"] = pd.to_datetime(df["post_date"])

st.title("Instagram Analytics Dashboard")
st.caption("Performance analysis of Instagram posts")

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

post_types = sorted(df["post_type"].dropna().unique())
selected_types = st.sidebar.multiselect(
    "Post Type",
    post_types,
    default=post_types
)

filtered_df = df[df["post_type"].isin(selected_types)].copy()

# -----------------------------
# KPI calculations
# -----------------------------
total_posts = len(filtered_df)
total_reach = filtered_df["reach"].sum()
total_likes = filtered_df["likes"].sum()
avg_engagement = filtered_df["engagement_rate"].mean() * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Posts", f"{total_posts:,}")
col2.metric("Total Reach", f"{total_reach:,.0f}")
col3.metric("Total Likes", f"{total_likes:,.0f}")
col4.metric("Avg Engagement", f"{avg_engagement:.2f}%")

st.divider()

# -----------------------------
# Engagement by Post Type
# -----------------------------
st.subheader("Engagement Rate by Post Type")

engagement = (
    filtered_df.groupby("post_type")["engagement_rate"]
    .mean()
    .sort_values(ascending=False)
    * 100
)

fig, ax = plt.subplots(figsize=(8, 4))
engagement.plot(kind="bar", ax=ax)
ax.set_ylabel("Average Engagement Rate (%)")
ax.set_xlabel("Post Type")
ax.set_title("Average Engagement by Post Type")
plt.xticks(rotation=0)
plt.tight_layout()

st.pyplot(fig)

# -----------------------------
# Monthly Engagement Trend
# -----------------------------
st.subheader("Monthly Engagement Trend")

filtered_df["month"] = filtered_df["post_date"].dt.to_period("M").astype(str)

monthly = (
    filtered_df.groupby("month")["engagement_rate"]
    .mean()
    .sort_index()
    * 100
)

fig, ax = plt.subplots(figsize=(10, 4))
monthly.plot(kind="line", marker="o", ax=ax)
ax.set_xlabel("Month")
ax.set_ylabel("Average Engagement Rate (%)")
ax.set_title("Monthly Engagement Trend")
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

# -----------------------------
# Reach vs Hashtags
# -----------------------------
st.subheader("Hashtags vs Reach")

fig, ax = plt.subplots(figsize=(8, 4))
ax.scatter(
    filtered_df["hashtag_count"],
    filtered_df["reach"],
    alpha=0.6
)

ax.set_xlabel("Number of Hashtags")
ax.set_ylabel("Reach")
ax.set_title("Hashtag Count vs Reach")
plt.tight_layout()

st.pyplot(fig)

# -----------------------------
# Top Posts
# -----------------------------
st.subheader("Top 10 Posts by Engagement")

top_posts = (
    filtered_df[
        [
            "post_id",
            "post_date",
            "post_type",
            "reach",
            "likes",
            "comments",
            "shares",
            "engagement_rate"
        ]
    ]
    .sort_values("engagement_rate", ascending=False)
    .head(10)
    .copy()
)

top_posts["engagement_rate"] = (
    top_posts["engagement_rate"] * 100
).round(2)

top_posts = top_posts.rename(
    columns={"engagement_rate": "engagement_rate (%)"}
)

st.dataframe(
    top_posts,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.caption(
    "Instagram Analytics | Python • Pandas • SQL • Excel • Data Visualization"
)
