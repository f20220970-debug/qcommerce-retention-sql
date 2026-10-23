-- Q3. The habit window: how many days do customers wait between orders?
-- Note: Instacart caps the gap at 30 days, so "30" means "30 days or more".
-- Technique: distribution with GROUP BY plus cumulative share via a running window SUM.
SELECT
    CAST(days_since_prior_order AS INTEGER)                         AS days_since_prior,
    COUNT(*)                                                        AS orders,
    ROUND(COUNT(*) * 1.0 / SUM(COUNT(*)) OVER (), 4)                AS share,
    ROUND(SUM(COUNT(*)) OVER (ORDER BY CAST(days_since_prior_order AS INTEGER))
          * 1.0 / SUM(COUNT(*)) OVER (), 4)                         AS cumulative_share
FROM orders
WHERE days_since_prior_order IS NOT NULL                            -- first orders have no gap
GROUP BY 1
ORDER BY 1;
