-- Q4. Retention curve: what share of customers reach their Nth order?
-- Instacart has no calendar dates, so retention is measured in orders, not weeks.
-- The dataset only includes customers with at least 4 orders, so the curve starts high:
-- treat it as "how deep do engaged customers go", not acquisition-to-repeat conversion.
WITH per_user AS (
    SELECT user_id, MAX(order_number) AS total_orders FROM orders GROUP BY user_id
),
milestones AS (SELECT UNNEST([2, 3, 5, 10, 20, 50, 100]) AS n)
SELECT
    n                                                        AS order_number,
    COUNT(*) FILTER (WHERE total_orders >= n)                AS customers_reaching,
    ROUND(COUNT(*) FILTER (WHERE total_orders >= n) * 1.0 / COUNT(*), 4) AS share_reaching
FROM milestones CROSS JOIN per_user
GROUP BY n
ORDER BY n;
