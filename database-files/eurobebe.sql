DROP DATABASE IF EXISTS eurobebe;
CREATE DATABASE eurobebe;
SHOW DATABASES;
USE eurobebe;

-- # USER:
-- ### User
CREATE TABLE User
(
    user_id    INT PRIMARY KEY,
    name       VARCHAR(50),
    age        INT,
    occupation VARCHAR(60),
    country    VARCHAR(50)
);

-- # DATA:
-- ### Year
CREATE TABLE Year
(
    year    INT PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES User (user_id)
        ON UPDATE cascade ON DELETE restrict
);

-- ### EUBirthData
CREATE TABLE EUBirthData
(
    eubd_id          INT PRIMARY KEY,
    country_code     VARCHAR(10),
    birth_rate       DECIMAL(5, 2),
    crude_birth_rate DECIMAL(5, 2),
    year             INT,
    FOREIGN KEY (year) REFERENCES Year (year)
        ON UPDATE cascade ON DELETE restrict
);

-- ### EUEmployment
CREATE TABLE EUEmployment
(
    eue_id            INT PRIMARY KEY,
    year              INT,
    country_code      VARCHAR(10),
    workforce         INT,
    self_employment   DECIMAL(5, 2),
    work_hours_weekly DECIMAL(5, 2),
    sex               VARCHAR(10),
    industry_sector   VARCHAR(85),
    FOREIGN KEY (year) REFERENCES Year (year)
        ON UPDATE cascade ON DELETE restrict
);

-- ### Children_FamilyBenefits
CREATE TABLE Children_FamilyBenefits
(
    cfb_id          INT PRIMARY KEY,
    year            INT,
    country_code    VARCHAR(10),
    support_program VARCHAR(85),
    dependent_type  VARCHAR(50),
    euro_amount     DECIMAL(10, 2),
    FOREIGN KEY (year) REFERENCES Year (year)
        ON UPDATE cascade ON DELETE restrict
);

-- # FEATURES:
-- ## Politicians:
-- PolicyAnalysis
CREATE TABLE PolicyAnalysis
(
    analysis_id  INT PRIMARY KEY,
    user_id      INT,
    country_code VARCHAR(10),
    FOREIGN KEY (user_id) REFERENCES User (user_id)
        ON UPDATE cascade ON DELETE restrict
);

-- ### PolicyDetails
CREATE TABLE PolicyDetails
(
    details_id           INT PRIMARY KEY,
    cost_per_month       DECIMAL(10, 2),
    policy_type          VARCHAR(50),
    effect_on_birth_rate DECIMAL(5, 2),
    analysis_id          INT,
    FOREIGN KEY (analysis_id) REFERENCES PolicyAnalysis (analysis_id)
        ON UPDATE cascade ON DELETE restrict
);

-- ## Daycare Operators:
-- ### BusinessPlanning
CREATE TABLE BusinessPlanning
(
    plan_id       INT PRIMARY KEY,
    daycare_id    INT,
    year_forecast INT,
    user_id       INT,
    FOREIGN KEY (user_id) REFERENCES User (user_id)
        ON UPDATE cascade ON DELETE restrict
);

-- GeneralLogistics 
CREATE TABLE GeneralLogistics
(
    oper_id            INT PRIMARY KEY,
    staffing_demand    INT,
    financial_analysis TEXT,
    plan_id            INT,
    FOREIGN KEY (plan_id) REFERENCES BusinessPlanning (plan_id)
        ON UPDATE cascade ON DELETE restrict
);

-- OperatingHours 
CREATE TABLE OperatingHours
(
    hours_id      INT PRIMARY KEY,
    plan_id       INT,
    year_forecast INT,
    daycare_id    INT,
    FOREIGN KEY (plan_id) REFERENCES BusinessPlanning (plan_id)
        ON UPDATE cascade ON DELETE restrict
);

-- ## Expecting Parents:
-- ### ChildcareOptions
CREATE TABLE ChildcareOptions
(
    option_id      INT PRIMARY KEY,
    country_code   VARCHAR(10),
    cost_per_month DECIMAL(10, 2),
    user_id        INT,
    FOREIGN KEY (user_id) REFERENCES User (user_id)
        ON UPDATE cascade ON DELETE restrict
);