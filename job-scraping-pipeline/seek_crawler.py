import requests
from bs4 import BeautifulSoup

#change seach field here, use "-" as separator
search_field = "assistant"
link = "https://www.seek.com.au/" + search_field+"-jobs"
r = requests.get(link)

#finds the number of pages of search results 
count = 1
exists = True
soups = []
while (exists):
    newlink = requests.get(link+"?page="+str(count))
    soup = BeautifulSoup(newlink.text, 'lxml')
    if "Sorry, we couldn't" in soup.find("h3").text:
        exists = False
    else:
        soups.append(soup)
        count += 1
        
#find a list of links to each job posting 
links = []
for soup in soups:
    a = soup.find_all("a")
    for item in a:
        if "href" in item.attrs and "data-automation" in item.attrs:
            if "/job" in item.attrs["href"] and "jobTitle" in item.attrs["data-automation"]:
                links.append(item.attrs["href"])
                
#extract information from each link 
title = []
company = []
city = []
jobinfo = []
texts = []
for i in range(400):
    r = requests.get(links[i])
    soup = BeautifulSoup(r.text, 'lxml')
    title.append(soup.find("h1").text)
    for item in soup.find_all("span"):
        if "data-automation" in item.attrs:
            if "advertiser-name" in item.attrs["data-automation"]:
                company.append(item.text) 
    info = ""
    count = 0
    for item in soup.find_all("div"):
        if "class" in item.attrs:
            if "o76g430" in item.attrs["class"]:
                if (count==0):
                    city.append(item.text)
                    count += 1
                else:
                    info+=(item.text) 
    jobinfo.append(info)
    text = ""
    for item in soup.find_all("div"):
        if "class" in item.attrs:
            if "_1v38w810" in item.attrs["class"]:
                text += item.text
    texts.append(text)
    
#put into dataframe
import pandas as pd
d = {"position title":title, "company name":company, "city":city, "additional information":jobinfo, "position information":texts}
df = pd.DataFrame(data=d)

pd.DataFrame.to_csv(df, "assistant-400.xlsx", index=False, encoding="UTF-8")

