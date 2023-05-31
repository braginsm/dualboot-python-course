DROP TABLE IF EXISTS employees;
CREATE TABLE "employees" (
  id serial PRIMARY KEY,
  name varchar,
  last_name varchar,
  hire_date date,
  salary int,
  email varchar
);
ALTER TABLE employees ADD COLUMN manager_id int REFERENCES employees (id);

DROP TABLE IF EXISTS departments;
CREATE TABLE "departments" (
  id serial PRIMARY KEY,
  name varchar,
  location_id int REFERENCES locations (id),
  manager_id int REFERENCES employees (id)
);
ALTER TABLE employees ADD COLUMN department_id int REFERENCES departments (id);