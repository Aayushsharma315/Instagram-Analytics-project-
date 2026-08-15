-- ============================================================
-- 02_analysis_queries.sql
-- Business-insight queries used for the README findings and
-- the Power BI / Tableau data model.
-- ============================================================

USE instagram_analytics;

-- 1) Average engagement rate by post type, ranked
SELECT
    post_type,
    COUNT(*)                         AS total_posts,
    ROUND(AVG(engagement_rate), 4)   AS avg_engagement_rate,
    ROUND(AVG(reach), 0)             AS avg_reach
FROM posts
GROUP BY post_type
ORDER BY avg_engagement_rate DESC;

-- 2) Best day + time bucket to post
SELECT
    day_of_week,
    time_bucket,
    ROUND(AVG(engagement_rate), 4) AS avg_engagement_rate,
    COUNT(*)                       AS n_posts
FROM posts
GROUP BY day_of_week, time_bucket
ORDER BY avg_engagement_rate DESC
LIMIT 10;

-- 3) Monthly engagement trend
SELECT
    year,
    month,
    SUM(total_engagement) AS monthly_engagement,
    SUM(reach)             AS monthly_reach
FROM posts
GROUP BY year, month
ORDER BY year, FIELD(month, 'January','February','March','April','May','June',
                            'July','August','September','October','November','December');

-- 4) Top 10 posts by engagement rate
SELECT post_id, post_type, post_date, reach, total_engagement, engagement_rate
FROM posts
ORDER BY engagement_rate DESC
LIMIT 10;

-- 5) Hashtag usage buckets vs average reach
SELECT
    CASE
        WHEN hashtag_count = 0 THEN '0 hashtags'
        WHEN hashtag_count BETWEEN 1 AND 3 THEN '1-3 hashtags'
        WHEN hashtag_count BETWEEN 4 AND 6 THEN '4-6 hashtags'
        ELSE '7+ hashtags'
    END AS hashtag_bucket,
    ROUND(AVG(reach), 0)           AS avg_reach,
    ROUND(AVG(engagement_rate), 4) AS avg_engagement_rate,
    COUNT(*)                       AS n_posts
FROM posts
GROUP BY hashtag_bucket
ORDER BY avg_reach DESC;

-- 6) Underperforming posts (bottom 10%) for content-strategy review
SELECT post_id, post_type, post_date, engagement_rate
FROM posts
WHERE engagement_rate <= (
    SELECT engagement_rate FROM posts
    ORDER BY engagement_rate
    LIMIT 1 OFFSET 62
)
ORDER BY engagement_rate ASC;
