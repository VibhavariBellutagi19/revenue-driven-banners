WITH banners_with_conversions AS (
    SELECT DISTINCT
        i.campaign_id,
        i.banner_id,
        conv.conversion_id
    FROM impressions i
    LEFT JOIN clicks c ON i.banner_id = c.banner_id AND i.campaign_id = c.campaign_id
    LEFT JOIN conversions conv ON c.click_id = conv.click_id
)
SELECT
    COUNT(DISTINCT CASE WHEN conversion_id IS NOT NULL THEN banner_id ELSE NULL END) AS number_of_banners_with_conversions
FROM banners_with_conversions
where campaign_id = {}
GROUP BY campaign_id
ORDER BY campaign_id;