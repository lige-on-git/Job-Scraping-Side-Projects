library(httr)
library(jsonlite)  # read and write json with R list
library(data.table)

setwd("/media/lige/Samsung2TB/Study_Data_of_Lige/2022/MAST90106_DS_Project/Job-Scraping-Side-Projects/job-scraping-pipeline")

## obtain skill api token

credential <- fread("../../emsi_skills_api_credentials.csv")
client.id <- credential$'Client ID'
secret <- credential$Secret
scope <- credential$Scope
url.token <- "https://auth.emsicloud.com/connect/token"

payload <- paste0('client_id=', client.id, '&client_secret=', secret,
                  '&grant_type=client_credentials&scope=', scope)
encode <- "form"
response.token <- VERB("POST", url.token, body = payload, 
                       add_headers(Content_Type = 'application/x-www-form-urlencoded'), 
                       content_type("application/x-www-form-urlencoded"), encode = encode)
token <- fromJSON(content(response.token, "text"))$access_token


## query all available skills

url.skills <- "https://emsiservices.com/skills/versions/latest/skills"

queryString <- list(
  fields = "id,name,type,infoUrl"
)

response.skills <- VERB("GET", url.skills, add_headers(Authorization = paste('Bearer', token)), 
                        query = queryString, content_type("application/octet-stream"))

all.skills <- fromJSON(content(response.skills, "text"))$data; head(all.skills)
all.skills.type <- all.skills["type"]

# -- add sub-data.frame to main data.table
all.skills <- setDT(all.skills[c("id","infoUrl","name")])
all.skills[, c('type_id', 'type_name') := all.skills.type$type[c('id', 'name')]]
head(all.skills)

fwrite(all.skills, "./data/skillset_list.csv")
