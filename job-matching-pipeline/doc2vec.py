import pandas as pd
from gensim.summarization import keywords
import matplotlib.pyplot as plt
import gensim
import os
from gensim import models
from sklearn.metrics.pairwise import cosine_distances
from sklearn.manifold import MDS
import numpy as np

df1 = pd.read_csv("../../Data/company_data/final_ds.csv",encoding='latin-1')
df2 = pd.read_csv("../../Data/Student Data/combined student data - processed.csv",encoding='latin-1')
df2 = df2.fillna("missing")

jd = df1['position information'].tolist()
companies = df1['company name'].tolist()
positions = df1['position title'].tolist()
name = df2["Name"].tolist()
last_name = df2["Last Name"].tolist()
role = df2["Roles applied for"].tolist()

# to list
studentdata = np.array(df2[["What gender do you identify as?", "Diversity", "Employment Status", "Education level", "Degree", "Associated Faculty", "Student Type?", "University/Institute", "Internship Type?"\
                             , "Reason to apply?", "Motivation to Apply?", "Scholarship"]])
studentdata = studentdata.tolist()
studentdata = [[' '.join(i)] for i in studentdata]

sdata = []
for i in range (len(studentdata)):
    sdata.append(studentdata[i][0])
studentdata = sdata

# 

data_student = []
for i in range(len(studentdata)):
    stu = models.doc2vec.TaggedDocument(words = studentdata[i].split(),tags = ['{}_{}'.format(name[i], i)])
    data_student.append(stu)
    
model = gensim.models.doc2vec.Doc2Vec(vector_size=50,min_count = 2,epochs= 40)
model.build_vocab(data_student)

model.train(data_student, total_examples=model.corpus_count, epochs=40)

datav = []
for i in range(len(data_student)):
    datav.append(model.docvecs[i])
 
model.infer_vector(jd[0].split()).shape
cos_dist =[]
for i in range(len(datav)):
    cos_dist.append(float(cosine_distances([model.infer_vector(jd[0].split())],[datav[i]])))
 
summary = pd.DataFrame({
        'Name': name,
        "Last Name": last_name,
        "Roles Applied": role,
        'Similarity': [ 1 - i for i in cos_dist],
        })
 
t = summary.sort_values('Similarity', ascending=False).head(5)
t["Ranking"] = range(1,6)

 
