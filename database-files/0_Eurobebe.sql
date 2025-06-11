DROP DATABASE IF EXISTS euro_database;
CREATE DATABASE IF NOT EXISTS euro_database;

USE euro_database;

-- # USER:
CREATE TABLE IF NOT EXISTS UserRoles
(
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS User
(
    user_id    INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name  VARCHAR(50),
    age        INT,
    occupation VARCHAR(60),
    country_code VARCHAR(10),
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES UserRoles (role_id)
        ON UPDATE cascade ON DELETE restrict
);

-- # DATA:

-- ### EUBirthData
CREATE TABLE IF NOT EXISTS EUBirthData
(
    eubd_id      INT AUTO_INCREMENT PRIMARY KEY,
    country_code VARCHAR(10),
    frequency    VARCHAR(10),
    year         INT,
    birth_rate   DECIMAL(5, 2),
    live_births  INT
);

-- ### EUEmployment
CREATE TABLE IF NOT EXISTS EUEmployment
(
    eue_id          INT AUTO_INCREMENT PRIMARY KEY,
    country_code    VARCHAR(10),
    country_name    VARCHAR(100),
    year            BIGINT,
    sex             VARCHAR(20),
    age_group       VARCHAR(20),
    cfw_full        DOUBLE, -- contributing family workers full-time
    cfw_part        DOUBLE, -- contributing family workers part-time
    cfw_total       DOUBLE,

    ecfw_full       DOUBLE, -- employed except contributing family workers full-time
    ecfw_part       DOUBLE,
    ecfw_total      DOUBLE,

    eee_full        DOUBLE, -- employed except employees full-time
    eee_part        DOUBLE,
    eee_total       DOUBLE,

    emp_full        DOUBLE,
    emp_part        DOUBLE,
    emp_total       DOUBLE,

    emp_ft          DOUBLE, -- employees full-time
    emp_pt          DOUBLE,
    emp_all         DOUBLE,

    self_full       DOUBLE,
    self_part       DOUBLE,
    self_total      DOUBLE,

    self_empr_full  DOUBLE, -- self-employed with employees full-time
    self_empr_part  DOUBLE,
    self_empr_total DOUBLE,

    self_own_full   DOUBLE, -- self-employed without employees full-time
    self_own_part   DOUBLE,
    self_own_total  DOUBLE
);


-- ### Children_FamilyBenefits
CREATE TABLE IF NOT EXISTS Children_FamilyBenefits
(
    cfb_id        INT AUTO_INCREMENT PRIMARY KEY,
    frequency     VARCHAR(10)    NOT NULL,
    scheme        VARCHAR(5)     NOT NULL,
    benefit_type  VARCHAR(30)    NOT NULL,
    target_group  VARCHAR(15)    NOT NULL,
    unit_measured VARCHAR(30)    NOT NULL,
    country_code  VARCHAR(2)     NOT NULL,
    year          INTEGER        NOT NULL,
    expenditure   NUMERIC(10, 2) NOT NULL
);

-- ### EUCPI
CREATE TABLE IF NOT EXISTS EUCPI
(
    eucpi_id     INT AUTO_INCREMENT PRIMARY KEY,
    country_name VARCHAR(100),
    year         INT,
    cpi_value    DECIMAL(6, 2)
);


-- # FEATURES:
-- ## Politicians:
-- PolicyAnalysis
CREATE TABLE IF NOT EXISTS PolicyAnalysis
(
    analysis_id  INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT,
    country_code VARCHAR(10),
    FOREIGN KEY (user_id) REFERENCES User (user_id)
        ON UPDATE cascade ON DELETE restrict
);

-- ### PolicyDetails
CREATE TABLE IF NOT EXISTS PolicyDetails
(
    details_id           INT AUTO_INCREMENT PRIMARY KEY,
    cost_per_month       DECIMAL(10, 2),
    policy_type          VARCHAR(50),
    effect_on_birth_rate DECIMAL(5, 2),
    analysis_id          INT,
    FOREIGN KEY (analysis_id) REFERENCES PolicyAnalysis (analysis_id)
        ON UPDATE cascade ON DELETE restrict
);

-- ## Daycare Operators:
-- ### BusinessPlanning
CREATE TABLE IF NOT EXISTS BusinessPlanning
(
    plan_id       INT AUTO_INCREMENT PRIMARY KEY,
    daycare_id    INT,
    year_forecast INT,
    user_id       INT,
    FOREIGN KEY (user_id) REFERENCES User (user_id)
        ON UPDATE cascade ON DELETE restrict
);

-- DaycareLocations
CREATE TABLE IF NOT EXISTS DaycareLocations
(
    daycare_id    INT AUTO_INCREMENT PRIMARY KEY,
    daycare_name VARCHAR(100),
    city          VARCHAR(100),
    country_code  VARCHAR(10),
    inactive BOOLEAN NOT NULL,
    owner_id INT,
    plan_id       INT,
    FOREIGN KEY (plan_id) REFERENCES BusinessPlanning (plan_id)
        ON UPDATE cascade ON DELETE restrict,
    FOREIGN KEY (owner_id) REFERENCES User (user_id)
        ON UPDATE cascade ON DELETE restrict
);

-- GeneralLogistics
CREATE TABLE IF NOT EXISTS GeneralLogistics
(
    oper_id            INT AUTO_INCREMENT PRIMARY KEY,
    staffing_demand    INT,
    financial_analysis TEXT,
    plan_id            INT,
    FOREIGN KEY (plan_id) REFERENCES BusinessPlanning (plan_id)
        ON UPDATE cascade ON DELETE restrict
);

-- OperatingHours
CREATE TABLE IF NOT EXISTS OperatingHours
(
    hours_id      INT AUTO_INCREMENT PRIMARY KEY,
    plan_id       INT,
    year_forecast INT,
    daycare_id    INT,
    FOREIGN KEY (plan_id) REFERENCES BusinessPlanning (plan_id)
        ON UPDATE cascade ON DELETE restrict
);

-- ## Expecting Parents:
-- ### ChildcareOptions
CREATE TABLE IF NOT EXISTS ChildcareOptions
(
    option_id      INT AUTO_INCREMENT PRIMARY KEY,
    country_code   VARCHAR(10),
    cost_per_month DECIMAL(10, 2),
    user_id        INT,
    FOREIGN KEY (user_id) REFERENCES User (user_id)
        ON UPDATE cascade ON DELETE restrict
);

-- Model 1 Weights
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