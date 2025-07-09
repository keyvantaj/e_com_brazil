\connect dash;

CREATE TABLE metrics (
    id SERIAL PRIMARY KEY,
    metric_name TEXT,
    value FLOAT
);