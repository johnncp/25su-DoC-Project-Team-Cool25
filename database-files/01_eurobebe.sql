DROP DATABASE IF EXISTS euro_database;
CREATE DATABASE IF NOT EXISTS euro_database;

USE euro_database;

-- # USER:
-- ### User
CREATE TABLE User
(
    user_id    INT AUTO_INCREMENT PRIMARY KEY,
    fname       VARCHAR(50),
    lname VARCHAR(50),
    country    VARCHAR(50),
    occupation VARCHAR(60),
);

-- # DATA:

-- ### EUBirthData
CREATE TABLE IF NOT EXISTS EUBirthData
(
    eubd_id          INT PRIMARY KEY,
    year             INT,
    country_code     VARCHAR(10),
    birth_rate       DECIMAL(5, 2),
    live_births DECIMAL(7,2),
    created_by       INT,
    FOREIGN KEY (created_by) REFERENCES User (user_id)
        ON UPDATE cascade ON DELETE set null
);

-- ### EUEmployment
CREATE TABLE IF NOT EXISTS EUEmployment
(
    eue_id            INT PRIMARY KEY,
    country_code      VARCHAR(10),
    year              INT,
    sex               VARCHAR(10),
    work_hours_weekly DECIMAL(5, 2),
    created_by        INT,
    FOREIGN KEY (created_by) REFERENCES User (user_id)
        ON UPDATE cascade ON DELETE set null
);

-- ### Children_FamilyBenefits
CREATE TABLE IF NOT EXISTS Children_FamilyBenefits
(
    cfb_id          INT PRIMARY KEY,
    benefit_type VARCHAR(100),
    target_group VARCHAR(100),
    unit_measured VARCHAR(100),
    country_code    VARCHAR(10),
    year            INT,
    expenditure DECIMAL(7,2),
    created_by      INT,
    FOREIGN KEY (created_by) REFERENCES User (user_id)
        ON UPDATE cascade ON DELETE set null
);

-- # FEATURES:
-- ## Politicians:
-- PolicyAnalysis
CREATE TABLE IF NOT EXISTS PolicyAnalysis
(
    policy_id  INT PRIMARY KEY,
    policy_name VARCHAR(50),
    focus_area VARCHAR(50),
    country_code VARCHAR(10),
    years INT,
    user_id      INT,
    FOREIGN KEY (user_id) REFERENCES User (user_id)
        ON UPDATE cascade ON DELETE restrict
);


-- ## Daycare Operators:

-- DaycareLocations
CREATE TABLE IF NOT EXISTS DaycareLocations
(
    daycare_id    INT PRIMARY KEY,
    daycare_name VARCHAR(100),
    opening_time  TIME,
    closing_time  TIME,
    monthly_price DECIMAL(7, 2),
    city          VARCHAR(50),
    country_code  VARCHAR(10),
    user_id       INT,
    FOREIGN KEY (user_id) REFERENCES User (user_id)
        ON UPDATE cascade ON DELETE restrict
);

-- ## Expecting Parents:
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


-- # INSERTING TEMPORARY "DATA":
-- ## Users (politicians, daycare operators, to-be parents)
INSERT INTO User (user_id, fname, lname, country, occupation)
VALUES (1, 'Mark', 'Fontenot', 'France', 'Politician'),
       (2, 'Eric', 'Gerber', 'Germany', 'Daycare Owner');

-- ## EUBirthData
INSERT INTO EUBirthData (eubd_id, year, country_code, birth_rate, live_births)
VALUES (1, 2023, 'BE', 10.8, 10.9),
       (2, 2024, 'DE', 9.3, 9.4);

-- ## EUEmployment
INSERT INTO EUEmployment (eue_id, country_code, year, sex, work_hours_weekly)
VALUES (1, 'BE', 2023, 'Female', 36.5),
       (2, 'DE', 2024, 'Male', 40.2);

-- ## Children_FamilyBenefits
INSERT INTO Children_FamilyBenefits (cfb_id, benefit_type, target_group, unit_measured, country_code, year, expenditure)
VALUES (1, 'Daycare Grant', 'Child under 18', 'Millions of euros', 'BE', 2020, 1912.12),
       (2, 'Parental Leave', 'Mothers', 'Millions of euros', 'DE', 2024, 25.00);

-- ## PolicyAnalysis
INSERT INTO PolicyAnalysis (analysis_id, policy_name, focus_area, country_code, year)
VALUES (1, 'Birth Rate Act', 'Day care grants', 'BE', 2021),
       (2, 'Parental Leave Bill', 'Parental Leave', 'DE', 2023);

-- ## DaycareLocations
INSERT INTO DaycareLocations (daycare_id, daycare_name, opening_time, closing_time, monthly_price, city, country_code)
VALUES (101, 'Little Child Daycare', 080000, 200000, 300.25, 'Brussels', 'BE'),
       (102, 'Happy Children Place', 090000, 160000, 256.78, 'Nice', 'FR');

-- ## AffinityResources
INSERT INTO AffinityResources(id, resource_name, reource_type, focus_area, country_code)
VALUES (1, 'Working Parent Association', 'Affinity Group', 'Working Parents', 'BE'),
(2, 'Foundation for Single Mothers', 'Charity', 'Single Mothers', 'FR');