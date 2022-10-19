## Create tables to store the enrolled student data
## Should only run the script for a single time

CREATE DATABASE students;
USE students;
SELECT database();

CREATE TABLE education (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uni_name VARCHAR(100),
    edu_level VARCHAR(100),
    degree VARCHAR(100)
);

CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(100)
);

CREATE TABLE students (
    id VARCHAR(20) NOT NULL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    linkedin VARCHAR(100),
    gender BOOL,
    age_upper int,
    reason LONGTEXT,
    motivation LONGTEXT,
    scholarship LONGTEXT,
    education_id INT,
    FOREIGN KEY(education_id) REFERENCES education(id)
);

-- junction tables
CREATE TABLE roles_students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20),
    role_id INT,
    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(role_id) REFERENCES roles(id)
);

SHOW TABLES;