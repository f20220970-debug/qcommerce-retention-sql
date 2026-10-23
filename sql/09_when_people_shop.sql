-- Q9. When do people shop? Orders by day of week and hour (Instacart codes day 0-6; the
-- dataset does not say which day is 0, so the day labels are left as numbers).
SELECT order_dow AS day_of_week, order_hour_of_day AS hour, COUNT(*) AS orders
FROM orders
GROUP BY 1, 2
ORDER BY 1, 2;
