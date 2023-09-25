WITH top_click_banners AS (
    SELECT 
        banner_id,
        campaign_id,
        rnk_click
    FROM (
        SELECT 
            banner_id,
            campaign_id,
            ROW_NUMBER() OVER(PARTITION BY campaign_id ORDER BY COUNT(click_id) DESC) AS rnk_click
        FROM clicks
        GROUP BY banner_id, campaign_id
    ) AS subquery
    WHERE rnk_click <= 5
),

remaining_banners AS (
    SELECT 
        banner_id,
        campaign_id,
        ROW_NUMBER() OVER(PARTITION BY campaign_id ORDER BY rand()) AS rnk_random
    FROM impressions
    WHERE NOT EXISTS (
        SELECT 1 FROM top_click_banners tcb 
        WHERE impressions.banner_id = tcb.banner_id AND impressions.campaign_id = tcb.campaign_id
    )
)

SELECT banner_id, campaign_id 
FROM top_click_banners

UNION ALL

SELECT banner_id, campaign_id 
FROM (
    SELECT 
        banner_id, 
        campaign_id,
        rnk_random,
        (5 - COALESCE(MAX(rnk_click) OVER(PARTITION BY campaign_id), 0)) AS banners_needed
    FROM remaining_banners
    LEFT JOIN top_click_banners ON remaining_banners.campaign_id = top_click_banners.campaign_id
) AS subquery
WHERE rnk_random <= banners_needed;
