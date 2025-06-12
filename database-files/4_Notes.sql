USE euro_database;

CREATE TABLE IF NOT EXISTS Notes
(
    note_id                INT AUTO_INCREMENT PRIMARY KEY,
    note_content           LONGTEXT,
    note_date_created      DATETIME NOT NULL,
    note_date_last_updated DATETIME NOT NULL,
    user_id INT NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);