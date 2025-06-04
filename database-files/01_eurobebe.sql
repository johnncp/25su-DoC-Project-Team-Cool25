DROP DATABASE IF EXISTS euro_database;
CREATE DATABASE IF NOT EXISTS euro_database;

USE euro_database;

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
CREATE TABLE IF NOT EXISTS Year
(
    year    INT PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES User (user_id)
        ON UPDATE cascade ON DELETE restrict
);

-- ### EUBirthData
CREATE TABLE IF NOT EXISTS EUBirthData
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
CREATE TABLE IF NOT EXISTS EUEmployment
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
CREATE TABLE IF NOT EXISTS Children_FamilyBenefits
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
CREATE TABLE IF NOT EXISTS PolicyAnalysis
(
    analysis_id  INT PRIMARY KEY,
    user_id      INT,
    country_code VARCHAR(10),
    FOREIGN KEY (user_id) REFERENCES User (user_id)
        ON UPDATE cascade ON DELETE restrict
);

-- ### PolicyDetails
CREATE TABLE IF NOT EXISTS PolicyDetails
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
CREATE TABLE IF NOT EXISTS BusinessPlanning
(
    plan_id       INT PRIMARY KEY,
    daycare_id    INT,
    year_forecast INT,
    user_id       INT,
    FOREIGN KEY (user_id) REFERENCES User (user_id)
        ON UPDATE cascade ON DELETE restrict
);

-- DaycareLocations
CREATE TABLE IF NOT EXISTS DaycareLocations
(
    daycare_id INT PRIMARY KEY,
    opening_time TIME,
    closing_time TIME,
    monthly_price DECIMAL(7,2),
    city VARCHAR(100),
    country_code VARCHAR(10)
);

-- GeneralLogistics 
CREATE TABLE IF NOT EXISTS GeneralLogistics
(
    oper_id            INT PRIMARY KEY,
    staffing_demand    INT,
    financial_analysis TEXT,
    plan_id            INT,
    FOREIGN KEY (plan_id) REFERENCES BusinessPlanning (plan_id)
        ON UPDATE cascade ON DELETE restrict
);

-- OperatingHours 
CREATE TABLE IF NOT EXISTS OperatingHours
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
CREATE TABLE IF NOT EXISTS ChildcareOptions
(
    option_id      INT PRIMARY KEY,
    country_code   VARCHAR(10),
    cost_per_month DECIMAL(10, 2),
    user_id        INT,
    FOREIGN KEY (user_id) REFERENCES User (user_id)
        ON UPDATE cascade ON DELETE restrict
);


-- # INSERTING TEMPORARY "DATA":
-- ## Users (politicians, daycare operators, to-be parents)
INSERT INTO User (user_id, name, age, occupation, country) VALUES
(1, 'Mark Fontenot', 80, 'Politician', 'France'),
(2, 'Eric Gerber', 80, 'Daycare Owner', 'Germany');

-- ## YEAR
INSERT INTO Year (year, user_id) VALUES
(2023, 1),
(2024, 2);

-- ## EUBirthData
INSERT INTO EUBirthData (eubd_id, country_code, birth_rate, crude_birth_rate, year) VALUES
(1, 'BE', 10.8, 10.9, 2023),
(2, 'DE', 9.3, 9.4, 2024);

-- ## EUEmployment
INSERT INTO EUEmployment (eue_id, year, country_code, workforce, self_employment, work_hours_weekly, sex, industry_sector) VALUES
(1, 2023, 'BE', 29500000, 11.2, 36.5, 'Female', 'Transportation'),
(2, 2024, 'DE', 44800000, 9.8, 35.2, 'Male', 'Finance');

-- ## Children_FamilyBenefits
INSERT INTO Children_FamilyBenefits (cfb_id, year, country_code, support_program, dependent_type, euro_amount) VALUES
(1, 2023, 'BE', '$ for families', 'Child under 18', 1912.12),
(2, 2024, 'DE', 'Alien Assistance', 'First and Second Child of Asylum Seekers', 25.00);

-- ## PolicyAnalysis
INSERT INTO PolicyAnalysis (analysis_id, user_id, country_code) VALUES
(1, 1, 'BE'),
(2, 2, 'DE');

-- ## PolicyDetails
INSERT INTO PolicyDetails (details_id, cost_per_month, policy_type, effect_on_birth_rate, analysis_id) VALUES
(1, 450.00, 'Universal Childcare', 2.3, 1),
(2, 320.00, 'Parental Leave', 1.8, 2);

-- ## BusinessPlanning
INSERT INTO BusinessPlanning (plan_id, daycare_id, year_forecast, user_id) VALUES
(1, 101, 2026, 2),
(2, 102, 2028, 2);

-- ## GeneralLogistics
INSERT INTO GeneralLogistics (oper_id, staffing_demand, financial_analysis, plan_id) VALUES
(1, 12, 'Projected: €580,000/year. Staff: €380,000. Operating: 1.5%', 1),
(2, 18, 'Expansion needs €250,000 investment.ROI: 22%', 2);

-- ## OperatingHours
INSERT INTO OperatingHours (hours_id, plan_id, year_forecast, daycare_id) VALUES
(1, 1, 2025, 101),
(2, 2, 2026, 102);

-- ## ChildcareOptions
INSERT INTO ChildcareOptions (option_id, country_code, cost_per_month, user_id) VALUES
(1, 'BE', 650.00, 1),
(2, 'DE', 450.00, 2);

-- ## DaycareLocations
INSERT INTO DaycareLocations (daycare_id, opening_time, closing_time, monthly_price, city, country_code) VALUES
(1, 080000, 200000, 300.25, 'Brussels', 'BE'),
(2, 090000, 160000, 256.78, 'Nice', 'FR');