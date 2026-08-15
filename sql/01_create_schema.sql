-- ============================================================
-- 01_create_schema.sql
-- Creates the database and table structure for Instagram
-- analytics in MySQL. Run this before loading the cleaned CSV.
-- ============================================================

CREATE DATABASE IF NOT EXISTS instagram_analytics;
USE instagram_analytics;

DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    post_id           VARCHAR(10)     PRIMARY KEY,
    post_date         DATETIME        NOT NULL,
    post_type         VARCHAR(20)     NOT NULL,
    caption           TEXT,
    hashtags          VARCHAR(255),
    hashtag_count     TINYINT         DEFAULT 0,
    reach             INT             NOT NULL,
    impressions        INT             NOT NULL,
    likes             INT             NOT NULL,
    comments          INT             DEFAULT 0,
    shares            INT             DEFAULT 0,
    saves             INT             DEFAULT 0,
    follows_gained    INT             DEFAULT 0,
    total_engagement  INT             NOT NULL,
    engagement_rate   DECIMAL(6,4)    NOT NULL,
    day_of_week       VARCHAR(10),
    hour              TINYINT,
    month             VARCHAR(15),
    year              SMALLINT,
    time_bucket       VARCHAR(10)
);

-- Load the cleaned CSV (adjust the path to your local machine).
-- Requires local_infile enabled on the MySQL server:
--   SET GLOBAL local_infile = 1;
LOAD DATA LOCAL INFILE 'data/processed/instagram_posts_clean.csv'
INTO TABLE posts
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(post_id, post_date, post_type, caption, hashtags, hashtag_count, reach,
 impressions, likes, comments, shares, saves, follows_gained,
 total_engagement, engagement_rate, day_of_week, hour, month, year, time_bucket);

-- Helpful indexes for the query patterns used in 02_analysis_queries.sql
CREATE INDEX idx_post_type ON posts (post_type);
CREATE INDEX idx_post_date ON posts (post_date);
CREATE INDEX idx_day_of_week ON posts (day_of_week);
