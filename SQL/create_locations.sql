CREATE TABLE "locations" (
  id serial PRIMARY KEY,
  address varchar,
  region_id int REFERENCES regions (id)
);