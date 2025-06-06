USE euro_database;


-- ### AffinityResources
CREATE TABLE IF NOT EXISTS AffinityResources
(
    id      INT PRIMARY KEY,
    resource_name VARCHAR(100),
    resource_type VARCHAR(50),
    focus_area VARCHAR(50),
    country_code   VARCHAR(10),
    user_id        INT,
    FOREIGN KEY (user_id) REFERENCES User (user_id)
        ON UPDATE cascade ON DELETE restrict
);

CREATE TABLE IF NOT EXISTS Policies
(
    policy_id  INT PRIMARY KEY,
    policy_name VARCHAR(50),
    focus_area VARCHAR(50),
    country_code VARCHAR(10),
    year INT,
    user_id      INT,
    FOREIGN KEY (user_id) REFERENCES User (user_id)
        ON UPDATE cascade ON DELETE restrict
);

INSERT INTO AffinityResources (id, resource_name, resource_type, focus_area, country_code)
VALUES(1, "Helping Parents", "Charity", "Working Parents", "BE"),
(2, "Supporting Mothers", "Affinity Group", "Single Mothers", "FR");