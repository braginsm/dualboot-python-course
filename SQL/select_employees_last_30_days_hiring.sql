SELECT *
FROM employees
WHERE hire_date >= CURRENT_DATE - interval '30' day;