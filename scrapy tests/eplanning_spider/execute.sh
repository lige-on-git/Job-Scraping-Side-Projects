#!/bin/sh

cd "/media/lige/Samsung2TB/Study_Data_of_Lige/2022/MAST90106_DS_Project/Job-Scraping-Side-Projects/scrapy tests/eplanning_spider"
scrapy crawl eplanning -O "./data/agent_info.json"
