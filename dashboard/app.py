import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# Page setup
# --------------------------------------------------
st.set_page_config(
    page_title="Instagram Analytics",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# Load data
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "processed" / "instagram_posts_clean.csv"

df = pd.read_csv(DATA_FILE)

df["post_date"] = pd.to_datetime(df["post_date"], errors="coerce")

# Remove invalid rows
df = df.dropna(subset=["post_date", "post_type"])

# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("Instagram Analytics")
st.caption("Content performance and engagement analysis")

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
st.sidebar.header("Dashboard Filters")

post_types = sorted(df["post_type"].dropna().unique())

selected_types = st.sidebar.multiselect(
    "Post Type",
    post_types,
    default=post_types
)

min_date = df["post_date"].min().date()
max_date = df["post_date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Handle date selection
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = min_date
    end_date = max_date

# --------------------------------------------------
# Filter data
# --------------------------------------------------
filtered_df = df[
    (df["post_type"].isin(selected_types)) &
    (df["post_date"].dt.date >= start_date) &
    (df["post_date"].dt.date <= end_date)
].copy()

# --------------------------------------------------
# Empty data check
# --------------------------------------------------
if filtered_df.empty:
    st.warning("No posts match the selected filters.")
    st.stop()

# --------------------------------------------------
# KPI calculations
# --------------------------------------------------
total_posts = len(filtered_df)
total_reach = filtered_df["reach"].sum()
total_likes = filtered_df["likes"].sum()
total_comments = filtered_df["comments"].sum()
avg_engagement = filtered_df["engagement_rate"].mean() * 100

# --------------------------------------------------
# KPI cards
# --------------------------------------------------
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Posts", f"{total_posts:,}")
c2.metric("Total Reach", f"{total_reach:,.0f}")
c3.metric("Total Likes", f"{total_likes:,.0f}")
c4.metric("Comments", f"{total_comments:,.0f}")
c5.metric("Avg Engagement", f"{avg_engagement:.2f}%")

st.divider()

# --------------------------------------------------
# Row 1 - Post Type + Engagement
# --------------------------------------------------
left, right = st.columns(2)

with left:
    st.subheader("Posts by Content Type")

    post_distribution = (
        filtered_df["post_type"]
        .value_counts()
        .sort_values(ascending=True)
    )

    fig, ax = plt.subplots(figsize=(7, 4))

    post_distribution.plot(
        kind="barh",
        ax=ax
    )

    ax.set_xlabel("Number of Posts")
    ax.set_ylabel("")
    ax.set_title("Content Distribution")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.subheader("Engagement by Content Type")

    engagement = (
        filtered_df.groupby("post_type")["engagement_rate"]
        .mean()
        .sort_values(ascending=False)
        * 100
    )

    fig, ax = plt.subplots(figsize=(7, 4))

    engagement.plot(
        kind="bar",
        ax=ax
    )

    ax.set_ylabel("Average Engagement (%)")
    ax.set_xlabel("")
    ax.set_title("Average Engagement Rate")

    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.divider()

# --------------------------------------------------
# Monthly performance
# --------------------------------------------------
st.subheader("Monthly Performance")

filtered_df["month"] = (
    filtered_df["post_date"]
    .dt.to_period("M")
    .astype(str)
)

monthly = (
    filtered_df.groupby("month")
    .agg(
        reach=("reach", "sum"),
        likes=("likes", "sum"),
        engagement=("engagement_rate", "mean")
    )
    .sort_index()
)

monthly["engagement"] = monthly["engagement"] * 100

fig, ax = plt.subplots(figsize=(12, 4))

ax.plot(
    monthly.index,
    monthly["engagement"],
    marker="o"
)

ax.set_xlabel("Month")
ax.set_ylabel("Average Engagement (%)")
ax.set_title("Monthly Engagement Trend")

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)
plt.close(fig)

st.divider()

# --------------------------------------------------
# Reach vs Likes
# --------------------------------------------------
left, right = st.columns(2)

with left:
    st.subheader("Reach vs Likes")

    fig, ax = plt.subplots(figsize=(7, 4))

    ax.scatter(
        filtered_df["reach"],
        filtered_df["likes"],
        alpha=0.65
    )

    ax.set_xlabel("Reach")
    ax.set_ylabel("Likes")
    ax.set_title("Reach and Like Relationship")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.subheader("Hashtags vs Reach")

    fig, ax = plt.subplots(figsize=(7, 4))

    ax.scatter(
        filtered_df["hashtag_count"],
        filtered_df["reach"],
        alpha=0.65
    )

    ax.set_xlabel("Number of Hashtags")
    ax.set_ylabel("Reach")
    ax.set_title("Hashtag Usage vs Reach")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.divider()

# --------------------------------------------------
# Top performing posts
# --------------------------------------------------
st.subheader("Top Performing Posts")

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
    .sort_values(
        "engagement_rate",
        ascending=False
    )
    .head(10)
    .copy()
)

top_posts["post_date"] = (
    top_posts["post_date"]
    .dt.strftime("%d %b %Y")
)

top_posts["engagement_rate"] = (
    top_posts["engagement_rate"] * 100
).round(2)

top_posts = top_posts.rename(
    columns={
        "post_id": "Post ID",
        "post_date": "Date",
        "post_type": "Type",
        "reach": "Reach",
        "likes": "Likes",
        "comments": "Comments",
        "shares": "Shares",
        "engagement_rate": "Engagement (%)"
    }
)

st.dataframe(
    top_posts,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# Quick insights
# --------------------------------------------------
st.divider()

st.subheader("Key Insights")

best_type = (
    filtered_df.groupby("post_type")["engagement_rate"]
    .mean()
    .idxmax()
)

best_engagement = (
    filtered_df.groupby("post_type")["engagement_rate"]
    .mean()
    .max() * 100
)

highest_reach_post = filtered_df.loc[
    filtered_df["reach"].idxmax()
]

i1, i2, i3 = st.columns(3)

i1.info(
    f"**Best Content Type**\n\n"
    f"{best_type} with an average engagement "
    f"of **{best_engagement:.2f}%**."
)

i2.info(
    f"**Highest Reach**\n\n"
    f"{highest_reach_post['reach']:,.0f} reached "
    f"on the highest-performing post."
)

i3.info(
    f"**Average Engagement**\n\n"
    f"Overall average engagement is "
    f"**{avg_engagement:.2f}%**."
)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.divider()

st.caption(
    "Instagram Analytics | Python • Pandas • Matplotlib • Streamlit"
)
