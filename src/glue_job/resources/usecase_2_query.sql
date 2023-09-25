WITH TopRevenueBanners AS (
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
FROM TopRevenueBanners
WHERE rnk_revenue <= {};