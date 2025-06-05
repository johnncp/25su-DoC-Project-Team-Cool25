USE euro_database;


-- ### AffinityResources
CREATE TABLE IF NOT EXISTS AffinityResources
(
    id      INT PRIMARY KEY,
    resource_name VARCHAR(100),
    reource_type VARCHAR(50),
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