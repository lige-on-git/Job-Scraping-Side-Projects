## packages, config, and shared utility functions

library("RMySQL")   # driver: need apt-get install libmariadbclient-dev & run install.packages("RMySQL")
library("data.table")
library("stringr")  # for string operations in R
library("ids")  # generate unique identifiers. https://www.rdocumentation.org/packages/ids/versions/1.0.1

# configs
mysql_credential_path <- "../../mysql-login.csv"
job_data_path <- "./data/final_ds.csv"
student_data_path <- "./data/combined student data - processed.csv"

search.key = "Data Science"

# database schema
db.user = fread(mysql_credential_path)$username
db.password = fread(mysql_credential_path)$password
db.host = fread(mysql_credential_path)$hostname

jobposts.schema <- list(
    'tools'=c(
        tool_name="VARCHAR(100)"), 
    'skills'=c(
        tool_name="VARCHAR(100)"),
    'companys'=c(
        company_name="VARCHAR(100)", 
        city="VARCHAR(100)"),
    'jobposts'=c(
        id="VARCHAR(100)",
        position_title="VARCHAR(100)", 
        position_info="LONGTEXT",
        extra_info="LONGTEXT",
        word_set="LONGTEXT", 
        company_id="INT", 
        job_id="INT"),
    'tools_posts'=c(
        jobpost_id="VARCHAR(20)", 
        tool_id="INT"), 
    'skills_posts'=c(
        jobpost_id="VARCHAR(20)", 
        skill_id="INT")
)


# remove space in the col names
# -- str_replace_all(s, pattern=" ", replacement="_")
remove_space <- function(DT){
  new_col_names <- lapply(names(DT), str_replace_all, pattern=" ", replacement="_")
  setnames(DT, unlist(new_col_names))
}

# remove uni-code & remove extra space by a single space
# -- iconv(s, "latin1", "ASCII", sub=" ")
# -- str_squish(s)
remove_unicode <- function(DT, col_name){
  # in-place removal of uni-code in a single column
  # <col_name>: in string - use get() to unpack column name from variable
  DT[, c(col_name) := lapply(.(get(col_name)), FUN=iconv, "latin1", "ASCII", sub=" ")]
  DT[, c(col_name) := lapply(.(get(col_name)), FUN=str_squish)]
}

remove_unicode_all <- function(DT){
  # in-place removal of uni-code in all columns
  DT[, names(DT) := lapply(.SD, FUN=iconv, "latin1", "ASCII", sub=" ")]
  DT[, names(DT) := lapply(.SD, FUN=str_squish)]
}

strlist_to_vec <- function(strlist){
  # convert string list to vector
  # <strlist>: can be a single string or a character vector (R has very well vector support)
  # e.g. change "['r', 'sql', 'python']" to c('r', 'sql', 'python')
  
  # - \\ means escape; | means or; s+ means more than one space (regular expression)
  strlist <- str_replace_all(string=strlist, pattern="\\[|\\]|\\'", replacement="")
  unlist(strsplit(x=strlist, split=",\\s+"))
}