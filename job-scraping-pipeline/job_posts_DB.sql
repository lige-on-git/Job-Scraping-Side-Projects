## Create tables to store the scrapped job posts data based on searching results
## Should only run the script for a single time

-- DROP DATABASE jobposts;
CREATE DATABASE jobposts;
USE jobposts;
SELECT database();

-- store searching keywords, e.g. data science, business analysis
CREATE TABLE jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job VARCHAR(100)
);

-- store company information
CREATE TABLE companys (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100),
    city VARCHAR(100)
);

-- store required skills
CREATE TABLE skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    skill_name VARCHAR(100)
);

-- store required tools
CREATE TABLE tools (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tool_name VARCHAR(100)
);

-- store posted job ads (should have time - maybe the next step)
CREATE TABLE jobposts (
    id VARCHAR(100) NOT NULL PRIMARY KEY,
    position_title VARCHAR(100),
    position_info LONGTEXT,
    extra_info LONGTEXT,
    word_set LONGTEXT,
    company_id INT,
    job_id INT,
    FOREIGN KEY(company_id) REFERENCES companys(id),
    FOREIGN KEY(job_id) REFERENCES jobs(id)
);

-- junction tables
CREATE TABLE tools_posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jobpost_id VARCHAR(20),
    tool_id INT,
    FOREIGN KEY(jobpost_id) REFERENCES jobposts(id),
    FOREIGN KEY(tool_id) REFERENCES tools(id)
);

CREATE TABLE skills_posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jobpost_id VARCHAR(20),
    skill_id INT,
    FOREIGN KEY(jobpost_id) REFERENCES jobposts(id),
    FOREIGN KEY(skill_id) REFERENCES skills(id)
);

SHOW TABLES;

-- SET GLOBAL local_infile=1;  -- otherwise will have "Loading local data is disabled" error when inserting in R

-- select count(*) from skills_posts;
-- DELETE FROM jobposts where job_id='1';
-- select count(*) from skills_posts;
-- DELETE FROM companys WHERE id=1;

-- select count(*) from companys where company_name='ABC' and city='Melbourne'
