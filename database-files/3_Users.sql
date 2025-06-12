USE euro_database;

-- UserRoles:
INSERT INTO UserRoles (role_name) VALUES
    ('daycare'),
    ('parent'),
    ('politician');

-- Users:

-- Daycare role users (role_id = 1)
INSERT INTO User (first_name, last_name, age, occupation, country_code, role_id)
VALUES
    ('Cara', 'Day', 34, 'Daycare Manager', 'DE', 1),
    ('Coak', 'Ceroe', 42, 'Early Childhood Educator', 'FR', 1),
    ('Crents', 'Manskuat-Rangel', 29, 'Daycare Assistant', 'SE', 1);

-- Parent role users (role_id = 2)
INSERT INTO User (first_name, last_name, age, occupation, country_code, role_id)
VALUES
    ('Eura', 'Pean', 38, 'Software Engineer', 'NL', 2),
    ('Dan', 'Kin', 41, 'Architect', 'IT', 2),
    ('Payne', 'Lovoane', 35, 'Marketing Manager', 'PL', 2);

-- Politician role users (role_id = 3)
INSERT INTO User (first_name, last_name, age, occupation, country_code, role_id)
VALUES
    ('Paul E.', 'Tishan', 45, 'City Council Member', 'BE', 3),
    ('Charles', 'Reuva', 52, 'Regional Parliament Member', 'ES', 3),
    ('Mish', 'O\'Hill', 48, 'Local Mayor', 'IE', 3);