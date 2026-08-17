--------------------------
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
