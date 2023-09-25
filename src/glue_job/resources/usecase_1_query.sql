WITH top_revenue_banners AS (
    SELECT
        banner_id,
        campaign_id,
        SUM(revenue) AS total_revenue,
        DENSE_RANK() OVER(PARTITION BY campaign_id ORDER BY SUM(revenue) DESC) AS rnk_revenue
    FROM conversions c
    JOIN clicks cl ON c.click_id = cl.click_id
    GROUP BY banner_id, campaign_id
)

SELECT banner_id, campaign_id
FROM top_revenue_banners
WHERE rnk_revenue <= 10
ORDER BY campaign_id, rnk_revenue;