## insert a whole csv file into a database

setwd("/media/lige/Samsung2TB/Study_Data_of_Lige/2022/MAST90106_DS_Project/Job-Scraping-Side-Projects/job-matching-pipeline")
source("table_separation.R")

# input csv data
job_data <- csv_input(job_data_path)

job_database_con <- database.connection('jobposts')
dbListTables(job_database_con)
dbListFields(job_database_con, name="jobposts")  # <jobposts> is a table name here

# -- Firstly insert to tables without FKs - c('tools', 'skills', 'companys', 'jobs')

tool_data <- tools.table(job_data)
insert2table(job_database_con, tool_data, jobposts.schema, "tools")

skill_data <- skills.table(job_data)
insert2table(job_database_con, skill_data, jobposts.schema, "skills")

company_data <- companys.table(job_data)
insert2table(job_database_con, company_data, jobposts.schema, "companys")

dbGetQuery(job_database_con, sprintf("insert into jobs (job) values ('%s');", search.key))

# -- Then insert to tables with FKs - c('jobposts', 'tools_posts', 'skills_posts')

post_data <- jobposts.table(job_data); names(post_data); nrow(post_data)
insert2table(job_database_con, post_data, jobposts.schema, "jobposts")

tool_post_data <- tools_posts.table(job_data)
insert2table(job_database_con, tool_post_data, jobposts.schema, "tools_posts")

skill_post_data <- skills_posts.table(job_data)
insert2table(job_database_con, skill_post_data, jobposts.schema, "skills_posts")
