# Dashboard Build Notes — Power BI & Tableau

Both dashboards use the same source file: `data/processed/instagram_posts_clean.csv`.

## Power BI

1. **Get Data → Text/CSV** → select `instagram_posts_clean.csv`.
2. Confirm data types on load: `post_date` as Date/Time, `reach`,
   `impressions`, `likes`, `comments`, `shares`, `saves`, `engagement_rate`
   as Whole Number / Decimal.
3. **Calculated measures (DAX)** — create these in a new measures table:

   ```
   Total Engagement = SUM(posts[total_engagement])
   Avg Engagement Rate = AVERAGE(posts[engagement_rate])
   Total Reach = SUM(posts[reach])
   Engagement per 1K Reach = DIVIDE([Total Engagement], [Total Reach]) * 1000
   ```

4. **Report pages:**
   - **Overview**: card visuals for Total Posts, Total Reach, Avg Engagement
     Rate, Total Follows Gained; a line chart of monthly engagement.
   - **Post Type Analysis**: clustered bar chart, engagement rate by
     `post_type`, sorted descending.
   - **Best Time to Post**: matrix/heatmap visual — rows `day_of_week`,
     columns `time_bucket`, values `Avg Engagement Rate` (conditional
     formatting: color scale).
   - **Top Posts**: table of top 10 posts by engagement rate, with
     `post_type` as a slicer.
5. Add a **slicer** for `post_type` and `month` on every page (sync slicers
   across pages via Format → Edit Interactions).
6. Publish and export as `.pbix` into this `dashboard/` folder before
   committing to GitHub, or link a Power BI Service published-report URL
   in the README.

## Tableau

1. **Connect → Text File** → `instagram_posts_clean.csv`.
2. Convert `post_date` to a Date dimension; verify `engagement_rate` is a
   Measure (Number, decimal).
3. **Calculated fields:**

   ```
   Engagement per 1K Reach:  ([total_engagement] / [reach]) * 1000
   ```

4. **Sheets to build:**
   - Bar chart: `AVG(engagement_rate)` by `post_type` (sort descending).
   - Heatmap: `day_of_week` (rows) × `time_bucket` (columns), color =
     `AVG(engagement_rate)`.
   - Line chart: `SUM(total_engagement)` by `MONTH(post_date)`.
   - Scatter plot: `hashtag_count` vs `reach`, with a trend line
     (Analytics pane → Trend Line → Linear).
5. Combine all four sheets into one **Dashboard**, add filters for
   `post_type` and `year`, and set filter actions so clicking a bar in the
   post-type chart filters the other sheets.
6. Publish to Tableau Public and add the embed/share link to the README,
   or export the packaged workbook (`.twbx`) into `dashboard/`.

## Screenshots

After building each dashboard, export a PNG screenshot into this folder
(`dashboard/powerbi_screenshot.png`, `dashboard/tableau_screenshot.png`)
and embed them in the main `README.md` — recruiters weigh a visible,
polished dashboard image heavily when scanning a portfolio repo.
