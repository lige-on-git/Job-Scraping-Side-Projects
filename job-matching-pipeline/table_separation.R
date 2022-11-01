## Insert and entire job-post csv file to the <jobposts> database
## Can only do this in an one-off operation like adding all existing data into the database.
## For appending further job-post data, run single_insert_jobposts.R

source("csv2database_utils.R")

csv_input <- function(path, id.byte=10){
  # <path>: of csv file; return a decoded DT object with unique identifier added
  # <id.byte>: size of the unique identifier
  DT <- fread(path, encoding='Latin-1')  # read and resolve (potential) encoding issues
  remove_space(DT)
  remove_unicode_all(DT)
  
  # add unique identifiers to all rows in the csv file (assume they're unique) 
  # -- random_id(n=3, bytes = 8)
  DT[, id := lapply(nrow(.SD), FUN=random_id, bytes = 10)]  # 'nrow(.SD') is the first input 'n' of random_id()
  nchar(random_id(bytes = 10))  # can use VARCHAR(20) in the database schema
  return(DT)
}

## insert data into MySQL database
## cheat sheet: https://gist.github.com/aravindhebbali/f2cc73794e9f9bfaa673
## for inserting data.frame: https://stackoverflow.com/questions/8864174/rmysql-dbwritetable-with-field-types
## also check ?dbWriteTable

# -- create a MySQL connection object (run MySQL script to create tables first)
database.connection <- function(db.name){
  # <db.name>: name of the database
  con <- dbConnect(
      MySQL(),
      user = db.user,
      password = db.password,
      host = db.host,
      dbname = db.name)
}

# -- table insertion wraper
insert2table <- function(db.connection, DT, schema, table.name){
  dbWriteTable(
    db.connection,
    name=table.name,
    value=DT,
    field.types = schema[table.name], 
    row.names=FALSE,
    append=TRUE
  )
}

# -- convert string list to vector to find unique tools and skills
tools.table <- function(jobpost.DT){
  # return a data.table to be inserted into the tools table in database
  tools <- strlist_to_vec(jobpost.DT[, tools_word_set])  # can pass a vector of strlist to it
  tools <- unique(tools)
  tool_data <- data.frame(tools)
  setnames(tool_data, "tool_name")   # set to the same name as database column
  return(tool_data)
}

# -- separating converted csv table into database tables

skills.table <- function(jobpost.DT){
  # return a data.table to be inserted into the skills table in database
  skills <- strlist_to_vec(jobpost.DT[, skills_word_set])
  skills <- unique(skills)
  skill_data <- data.frame(skills)
  setnames(skill_data, "skill_name")
  return(skill_data)
}

companys.table <- function(jobpost.DT){
  # return a data.table to be inserted into the companys table in database
  company_data <- jobpost.DT[, .(company_name, city)]
  unique(company_data, by=c("company_name", "city"))
}

jobposts.table <- function(jobpost.DT){
  # return a data.table to be inserted into the jobposts table in database
  post_data <- jobpost.DT[, .(
      id,  # unique identifier of job post
      company_name,  # use it to join with companys table
      city,          # use it to join with companys table
      position_title, 
      position_info = position_information,  # names to match database columns
      extra_info = additional_information,
      word_set = jd_word_set)]
  post_data[, job := search.key]  # job name is the search key - use it to join with jobs table
  
  # need to join with companys and jobs to acquire their auto-increment id as FK
  company_df <- dbReadTable(job_database_con, name="companys"); names(company_df)
  job_df <- dbReadTable(job_database_con, name="jobs")
  
  post_data <- post_data[company_df, on=c('company_name', 'city'), nomatch = 0]
  setnames(post_data, old='i.id', new='company_id')  # add company id
  
  post_data <- post_data[job_df, on=('job'), nomatch = 0]
  setnames(post_data, old='i.id', new='job_id')      # add job id
  post_data <- post_data[, .(
      id,
      position_title, 
      position_info, 
      extra_info, 
      company_id, job_id)]
}

# -- need to join jobposts table with tools and skills tables to construct 2 many-to-many junction tables
# -- tools_posts junction table
tools_posts.table <- function(jobpost.DT){
  # return a data.table to be inserted into the tools_posts junction table in database
  post_data <- job_data[, .(tool_name = strlist_to_vec(tools_word_set)), by=id]
  tool_df <- dbReadTable(job_database_con, name="tools"); setDT(tool_df); names(tool_df)
  
  # join two "many" sides to match their PKs (as 2 FKs in the junction table)
  tools_posts_junct <- post_data[tool_df, on=c("tool_name")]; nrow(tools_posts_junct)
  setnames(tools_posts_junct, old=c('id'), new='jobpost_id')
  setnames(tools_posts_junct, old=c('i.id'), new='tool_id'); names(tools_posts_junct); 
  tool_post_data <- tools_posts_junct[, .(jobpost_id, tool_id)]
}

# -- skills_posts junction table (stores PK of skills and jobposts tables)
skills_posts.table <- function(jobpost.DT){
  # return a data.table to be inserted into the skills_posts junction table in database
  post_data <- job_data[, .(skill_name = strlist_to_vec(skills_word_set)), by=id]
  skill_df <- dbReadTable(job_database_con, name="skills"); setDT(skill_df); names(skill_df)
  skills_posts_junct <- post_data[skill_df, on=c("skill_name")]; nrow(skills_posts_junct)
  setnames(skills_posts_junct, old=c('id'), new='jobpost_id')
  setnames(skills_posts_junct, old=c('i.id'), new='skill_id'); names(skills_posts_junct)
  skill_post_data <- skills_posts_junct[, .(jobpost_id, skill_id)]
}
