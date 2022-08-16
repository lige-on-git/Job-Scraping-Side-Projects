#!/bin/sh

# get into virtual env
conda info --envs
conda activate scrapy37

cd "/media/lige/Samsung2TB/Study_Data_of_Lige/2022/MAST90106_DS_Project/Job-Scraping-Side-Projects/scrapy tests/"
scrapy startproject quotes_spider  # start a project - quotes_spider
cd quotes_spider/quotes_spider/spiders/
scrapy genspider quotes quotes.toscrape.com  # initialize a spider - quotes

# get into scrapy shell
scrapy shell
fetch("http://quotes.toscrape.com/")
response
response.xpath('//h1/a/text()').extract()[0]  # extract text from a html tag
len(response.xpath('//*[@class="tag"]'))
len(response.xpath('//*[@class="tag-item"]'))
response.xpath('//*[@class="tag-item"]/a/text()').extract()  # extract text from a html class
exit()

# use the shell commands to supplement the spider
# then run the spider
scrapy list
scrapy crawl quotes
