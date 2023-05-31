SELECT d.name, MAX(e.salary) as max_salary, MIN(e.salary) as min_salary
FROM employees e
JOIN departments d ON e.department_id = d.id
GROUP BY d.id;