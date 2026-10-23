-- Q6. Width = wallet share: do customers who buy across more categories in their FIRST order
-- go on to place more orders?
-- Caveat: this is correlation, not causation (bigger first baskets may simply come from
-- more committed households). The honest next step would be an experiment, for example
-- nudging first-time buyers to add one item from a new category and comparing repeat rates.
WITH first_orders AS (
    SELECT order_id, user_id FROM orders WHERE order_number = 1
),
first_breadth AS (
    SELECT fo.user_id, COUNT(DISTINCT p.department_id) AS departments_in_first_order
    FROM first_orders fo
    JOIN order_items oi ON oi.order_id = fo.order_id
    JOIN products p     ON p.product_id = oi.product_id
    GROUP BY fo.user_id
),
totals AS (SELECT user_id, MAX(order_number) AS total_orders FROM orders GROUP BY user_id)
SELECT
    CASE WHEN departments_in_first_order >= 7 THEN '7+'
         ELSE CAST(departments_in_first_order AS VARCHAR) END        AS departments_in_first_order,
    COUNT(*)                                                          AS customers,
    ROUND(MEDIAN(total_orders), 1)                                    AS median_total_orders,
    ROUND(AVG(total_orders), 2)                                       AS avg_total_orders,
    ROUND(AVG(CASE WHEN total_orders >= 10 THEN 1 ELSE 0 END), 4)     AS share_reaching_10_orders
FROM first_breadth fb JOIN totals t USING (user_id)
GROUP BY 1
ORDER BY MIN(departments_in_first_order);
