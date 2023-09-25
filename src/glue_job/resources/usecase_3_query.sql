WITH TopRevenueBanners AS (
    SELECT
        banner_id,
        campaign_id,
        DENSE_RANK() OVER(PARTITION BY campaign_id ORDER BY SUM(revenue) DESC) AS rnk_revenue
    FROM conversions c
    JOIN clicks cl ON c.click_id = cl.click_id
    GROUP BY banner_id, campaign_id
),
FilteredRevenueBanners AS (
    SELECT banner_id, campaign_id,rnk_revenue
    FROM TopRevenueBanners
    WHERE rnk_revenue <= {}
),

TopClickBanners AS (
    SELECT
        cl.banner_id,
        cl.campaign_id,
        DENSE_RANK() OVER(PARTITION BY cl.campaign_id ORDER BY COUNT(cl.click_id) DESC) AS rnk_click
    FROM clicks cl
    WHERE NOT EXISTS (
        SELECT 1
        FROM FilteredRevenueBanners frb
        WHERE frb.banner_id = cl.banner_id AND frb.campaign_id = cl.campaign_id
    )
    GROUP BY cl.banner_id, cl.campaign_id
),
FilteredClickBanners AS (
    SELECT banner_id, campaign_id,rnk_click
    FROM TopClickBanners
    WHERE rnk_click <= {}
)

SELECT banner_id, campaign_id FROM FilteredRevenueBanners
UNION ALL
SELECT banner_id, campaign_id FROM FilteredClickBanners