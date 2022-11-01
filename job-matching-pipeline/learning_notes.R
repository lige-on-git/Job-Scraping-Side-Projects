## Some interesting notes:

job_data <- csv_input(job_data_path)

# -- expand tools and skills lists in post_data
# -- here is a very interesting difference between lapply() and applying a function directly in a DT
job_data[2, .(tools = lapply(tools_word_set, FUN=strlist_to_vec))]
job_data[2, .(tools = strlist_to_vec(tools_word_set))]  # can use this to unpack a string list to multiple rows

# -- this is due to different behaviors of lapply and applying a function directly in a DT
strlist_to_vec(job_data[, tools_word_set])  # strlist_to_vec() unlists all elements into a single vector
lapply(job_data[, tools_word_set], strlist_to_vec)  # strlist_to_vec() only unlists a row into a vector

# -- can use "by" to constrain FUN to each job post, so only expand tools list within each job post
post_data <- job_data[, .(tool_name = strlist_to_vec(tools_word_set)), by=id]
names(post_data); nrow(post_data)