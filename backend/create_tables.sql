CREATE DATABASE study_planner;
USE study_planner;
SHOW DATABASES;
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_date DATE,
    task_name TEXT,
    estimated_minutes INT,
    is_completed BOOLEAN DEFAULT FALSE
);
SHOW TABLES;
DESCRIBE tasks;
SELECT * FROM tasks;

