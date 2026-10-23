-- Q7. First basket vs long-term behaviour: does the size of the first order predict loyalty?
-- Technique: CTEs, CASE bucketing, MEDIAN.
WITH first_size AS (
    SELECT o.user_id, COUNT(*) AS first_basket_items
    FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.order_number = 1
    GROUP BY o.user_id
),
totals AS (SELECT user_id, MAX(order_number) AS total_orders FROM orders GROUP BY user_id)
SELECT
    CASE WHEN first_basket_items <= 5  THEN '1-5 items'
         WHEN first_basket_items <= 10 THEN '6-10 items'
         WHEN first_basket_items <= 20 THEN '11-20 items'
         ELSE '21+ items' END                                     AS first_basket,
    COUNT(*)                                                      AS customers,
    ROUND(MEDIAN(total_orders), 1)                                AS median_total_orders,
    ROUND(AVG(CASE WHEN total_orders >= 10 THEN 1 ELSE 0 END), 4) AS share_reaching_10_orders
FROM first_size JOIN totals USING (user_id)
GROUP BY 1
ORDER BY MIN(first_basket_items);
