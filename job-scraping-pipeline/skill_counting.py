import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import collections
import matplotlib.pyplot as plt

df = pd.read_excel("data engineer-400.xlsx")
data = df.copy()
data.drop_duplicates(subset=['position information'], inplace=True, ignore_index=True)

positions = data['position information']
positions_edited = []
lemmatizer = WordNetLemmatizer()
for i in range(len(positions)): 
    position = str(positions[i])
    pattern = r'[^A-Za-z\s\n\t]'
    replace = ''
    remove_non_alphabetic = re.sub(pattern, replace, position) # remove non-alphabetic characters
    pattern = r'\s+'
    replace = ' '
    remove_extra_space = re.sub(pattern, replace, remove_non_alphabetic) # remove extra spaces
    txt_lower = remove_extra_space.lower() # to lowercase 
    wordList = nltk.word_tokenize(txt_lower) # tokenize
    stopWords = set(stopwords.words('english'))
    filteredList = [w.lower() for w in wordList if not w in stopWords] # remove stop words and cast to lower case 
    positions_edited.append(' '.join([lemmatizer.lemmatize(w) for w in filteredList if len(w)>1])) 
    
skills = pd.read_csv("skillset_list.csv")

skill_names = skills['name']
skill_types = skills['type.name']
frequency_certification = {}
frequency_common_skill = {}
frequency_specialized_skill ={}
for i in range(len(positions_edited)):
    position = positions_edited[i]
    for i in range(len(skill_names)):
        skill = skill_names[i]
        if skill.lower() in position:
            if skill_types[i] == "Certification":
                if skill not in frequency_certification:
                    frequency_certification[skill] = 1
                else:
                    frequency_certification[skill] += 1
            elif skill_types[i] == "Common Skill":
                if skill not in frequency_common_skill:
                    frequency_common_skill[skill] = 1
                else:
                    frequency_common_skill[skill] += 1
            else:
                if skill not in frequency_specialized_skill:
                    frequency_specialized_skill[skill] = 1
                else:
                    frequency_specialized_skill[skill] += 1
                    
sorted_frequency_certification = collections.OrderedDict(frequency_certification)
sorted_frequency_common_skill = collections.OrderedDict(frequency_common_skill)
sorted_frequency_specialized_skill = collections.OrderedDict(frequency_specialized_skill)

skill_counts = pd.DataFrame([sorted_frequency_certification,sorted_frequency_common_skill])

plt.plot(sorted(frequency_common_skill, key=frequency_common_skill.get, reverse=True)[:10],
         sorted(frequency_common_skill.values(), reverse=True)[:10])
ax = plt.gca()
plt.draw()
ax.set_xticklabels(sorted(frequency_common_skill, key=frequency_common_skill.get, reverse=True)[:10],rotation = 90)

plt.plot(sorted(frequency_specialized_skill, key=frequency_specialized_skill.get, reverse=True)[:10],
         sorted(frequency_specialized_skill.values(), reverse=True)[:10])
ax = plt.gca()
plt.draw()
ax.set_xticklabels(sorted(frequency_specialized_skill, key=frequency_specialized_skill.get, reverse=True)[:10],rotation = 90)

