-- Q8. Habit products: the items customers come back for again and again.
-- Only products bought at least 5,000 times, so small products with lucky streaks don't dominate.
-- Technique: HAVING, ranking within department with ROW_NUMBER() OVER (PARTITION BY ...).
WITH product_stats AS (
    SELECT p.product_name, d.department,
           COUNT(*) AS times_bought, AVG(oi.reordered) AS reorder_rate
    FROM order_items oi
    JOIN products p    ON p.product_id = oi.product_id
    JOIN departments d ON d.department_id = p.department_id
    GROUP BY p.product_name, d.department
    HAVING COUNT(*) >= {min_count}
),
ranked AS (
    SELECT *, ROW_NUMBER() OVER (ORDER BY reorder_rate DESC) AS overall_rank,
              ROW_NUMBER() OVER (PARTITION BY department ORDER BY reorder_rate DESC) AS rank_in_department
    FROM product_stats
)
SELECT product_name, department, times_bought, ROUND(reorder_rate, 4) AS reorder_rate, overall_rank
FROM ranked
WHERE overall_rank <= 20
ORDER BY overall_rank;
