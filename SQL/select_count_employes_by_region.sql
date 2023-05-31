SELECT r.name, COUNT(e.id)
FROM employees e
JOIN departments d ON e.department_id = d.id
JOIN locations l ON d.location_id = l.id
JOIN regions r ON l.region_id = r.id
GROUP BY r.id;