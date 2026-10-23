-- Q2. Which categories build habits? Reorder rate and share of volume by department.
-- Technique: JOINs, GROUP BY, and a window function (SUM() OVER ()) for share of total.
SELECT
    d.department,
    COUNT(*)                                            AS items_sold,
    ROUND(COUNT(*) * 1.0 / SUM(COUNT(*)) OVER (), 4)    AS share_of_items,
    ROUND(AVG(oi.reordered), 4)                         AS reorder_rate
FROM order_items oi
JOIN products p     ON p.product_id = oi.product_id
JOIN departments d  ON d.department_id = p.department_id
GROUP BY d.department
ORDER BY reorder_rate DESC;
