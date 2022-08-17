#!/bin/sh

# get into virtual env
conda info --envs
conda activate scrapy37

cd "/media/lige/Samsung2TB/Study_Data_of_Lige/2022/MAST90106_DS_Project/Job-Scraping-Side-Projects/scrapy tests/"
scrapy startproject quotes_spider  # start a project - quotes_spider
cd quotes_spider/quotes_spider/spiders/
scrapy genspider quotes quotes.toscrape.com  # initialize a spider - quotes

# _________________________________
# get into scrapy shell (a python console - see scrapy_shell_commands.py)
scrapy shell
exit()

# use the tested scrapy shell commands to supplement the spider
# then run the spider after getting into the root directory of the spider
cd "/media/lige/Samsung2TB/Study_Data_of_Lige/2022/MAST90106_DS_Project/Job-Scraping-Side-Projects/scrapy tests/quotes_spider/"
scrapy list
scrapy crawl quotes

# export to the root directory of the spider
scrapy crawl quotes -o quotes.csv  # export csv - seems to be more prone to errors than json when separating elements
scrapy crawl quotes -o quotes.json  # export json

# export to a specific directory - a better practice, as can gitignore the data directory
scrapy crawl quotes -o "./data/quotes.csv"
scrapy crawl quotes -o "./data/quotes.json"
