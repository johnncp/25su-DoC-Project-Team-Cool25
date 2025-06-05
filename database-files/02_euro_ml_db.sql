DROP DATABASE IF EXISTS euro_ml_db;
CREATE DATABASE IF NOT EXISTS euro_ml_db;

USE euro_ml_db;

CREATE TABLE IF NOT EXISTS Model1Weights
(
    weight_id    INT AUTO_INCREMENT PRIMARY KEY,
    feature_name VARCHAR(100)   NOT NULL,
    weight       DECIMAL(10, 6) NOT NULL
);

INSERT INTO Model1Weights (feature_name, weight)
VALUES ('intercept', 7.152300),
       ('weekly_hours', 0.031100),
       ('cash_per_capita', 0.063800),
       ('maternity_per_capita', -0.057400),
       ('services_per_capita', 0.000200),
       ('weekly_hours_squared', 0.100900),
       ('weekly_hours_cubed', -0.075300),
       ('cash_per_capita_squared', -0.015800),
       ('services_per_capita_squared', 0.000050);
