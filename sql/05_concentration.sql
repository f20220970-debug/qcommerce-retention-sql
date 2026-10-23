-- Q5. How concentrated is the business? Share of orders from the most frequent customers.
-- Technique: NTILE window function to split customers into 10 equal groups by order count.
WITH per_user AS (
    SELECT user_id, COUNT(*) AS orders FROM orders GROUP BY user_id
),
deciles AS (
    SELECT *, NTILE(10) OVER (ORDER BY orders DESC) AS decile FROM per_user
)
SELECT
    decile,
    COUNT(*)                                              AS customers,
    SUM(orders)                                           AS orders,
    ROUND(SUM(orders) * 1.0 / SUM(SUM(orders)) OVER (), 4) AS share_of_orders,
    ROUND(SUM(SUM(orders)) OVER (ORDER BY decile) * 1.0 / SUM(SUM(orders)) OVER (), 4) AS cumulative_share,
    ROUND(AVG(orders), 1)                                 AS avg_orders
FROM deciles
GROUP BY decile
ORDER BY decile;
