-- Q1. How big is the business, and how much of it is repeat buying?
-- Technique: aggregates across joined tables.
WITH baskets AS (
    SELECT order_id, COUNT(*) AS items, SUM(reordered) AS reordered_items
    FROM order_items GROUP BY order_id
)
SELECT
    (SELECT COUNT(DISTINCT user_id) FROM orders)              AS customers,
    (SELECT COUNT(*) FROM orders)                             AS orders,
    (SELECT COUNT(*) FROM products)                           AS products,
    ROUND(AVG(items), 2)                                      AS avg_items_per_order,
    ROUND(SUM(reordered_items) * 1.0 / SUM(items), 4)         AS share_items_reordered,
    (SELECT ROUND(AVG(n), 2) FROM (SELECT COUNT(*) AS n FROM orders GROUP BY user_id)) AS avg_orders_per_customer
FROM baskets;
