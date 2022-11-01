import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import nltk
import string
from nltk.tokenize import word_tokenize
import math
from nltk import pos_tag
from nltk.stem import PorterStemmer
from plotly.offline import download_plotlyjs, plot, iplot
import plotly.graph_objs as go
from manual_skillset import *

# read raw data
data_scientist = pd.read_excel('../Data/data scientist-400.xlsx')
business_analyst = pd.read_excel('../Data/business analyst-300.xlsx')
data_engineer = pd.read_excel('../Data/data engineer-400.xlsx')
assistant = pd.read_excel('../Data/assistant-400.xlsx')
software_engineer = pd.read_excel('../Data/software engineer-400.xlsx')

ps = PorterStemmer()

# remove duplicate
def remove_duplicate(raw_data):
    new_data = raw_data.drop_duplicates(subset=['position title', 'company name', 
                                                'city', 'position information'])
    return new_data
    
# tokenize + filter + stem 
def prepare_job_desc(jd):
    
    # tokenize
    tokens = word_tokenize(jd.replace('?','').replace('!','').replace('&','')
                           .replace('-','').replace(',','').replace('.','')
                           .replace('@','').replace('%','').replace('(','')
                           .replace(')','').replace(':','').replace('$','')
                           .replace("'",'').replace('’','').replace('/','')
                           .replace('+',''))
    # assign tags
    token_tag = pos_tag(tokens)
    
    # filter tags
    include_tags = ['VBN', 'VBD', 'JJ', 'JJS', 'JJR', 'CD', 'NN', 'NNS', 'NNP', 'NNPS']
    filtered_tokens = [tok for tok, tag in token_tag if tag in include_tags]
    
    # stem words
    ps = PorterStemmer()
    stemmed_tokens = [ps.stem(tok).lower() for tok in filtered_tokens]
    return list(set(stemmed_tokens))

# create new column
def new_wordset(preprocessed_data):
    new_data_copy = preprocessed_data.copy()
    new_data_copy['jd_word_set'] = preprocessed_data['position information'].map(prepare_job_desc)
    return new_data_copy
    
tools_all = []
skills_all = []
def add_new_wordset(prep_data):
    
    new_pre_data = prep_data.copy()
    
    for i in range(len(prep_data)):
        tool_list = []
        skill_list = []
        job_desc = prep_data.iloc[i]['position information'].lower()
        job_desc_set = list(prep_data.iloc[i]['jd_word_set'])
        #print(prep_data.iloc[2]['jd_word_set'])

        # check if the keywords are in the job description
        tool_words = tools1_set.intersection(job_desc_set)
        skill_words = skills1_set.intersection(job_desc_set)

        # check if longer keywords are in the jd
        for tools in tools1: # longer tools words
            if tools in job_desc:
                tool_list.append(tools)
        for skills in skills1: # longer skills words
            if skills in job_desc:
                skill_list.append(skills)


        tool_list += list(tool_words)
        skill_list += list(skill_words)
        
        
        tools_all.append(tool_list)
        skills_all.append(skill_list)
        
        if len(tool_list) == 0:
            tool_list.append('nothing specified')
        
        if len(skill_list) == 0:
            skill_list.append('nothing specified')
        
    new_pre_data['tools_word_set'] = tools_all
    new_pre_data['skills_word_set'] = skills_all
        
    
    return new_pre_data

ba_new = remove_duplicate(business_analyst)
ba_preprocessed = new_wordset(ba_new)
ba1 = add_new_wordset1(ba_preprocessed)
ba1.to_csv('final_ds.csv', index = False)



