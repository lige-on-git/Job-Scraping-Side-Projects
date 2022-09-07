#!/bin/sh

# run a stand-alone scrapy script
scrapy runspider books_scrapy.py -O "./data/books_by_scrapy.csv"
