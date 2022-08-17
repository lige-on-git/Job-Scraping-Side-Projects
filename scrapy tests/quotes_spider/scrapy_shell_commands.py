## test scraping scripts within a scrapy shell (a python console)
# _________________________________
## HTML review:
# <p align="center">This is paragraph.</p>
# Tag: <p> </p>
# Element: This is paragraph.
# Attribute: align

# to fetch html which is then stored in <response> variable
fetch("http://quotes.toscrape.com/")

# _________________________________
## A double slash "//" means any descendant node of the current node in the HTML tree which matches the locator
## A single slash "/" means a node which is a direct child of the current.

# locate from nested tag selectors
response.xpath('//h1/a/text()').extract()[0]

# locate from a single class attribute selector
len(response.xpath('//*[@class="tag"]'))
len(response.xpath('//*[@class="tag-item"]'))

# locate from nested class attribute selectors (then extract text)
response.xpath('//*[@class="quote"]//*[@class="tag"]/text()').extract()

# locate from nested class attribute and tag selectors (then extract text)
response.xpath('//*[@class="tag-item"]/a/text()').extract()
response.xpath('//span/*[@class="author"]/text()').extract()

# locate from parallel selectors on the same level (then extract text)
response.xpath('//span[@class="text"]/text()').extract()

# _________________________________
## extract contents:
# 1. extract text element
response.xpath('//*[@class="tags"]/a/text()').extract()
# 2. extract content of an attribute
response.xpath('//*[@class="tags"]/a/@href').extract()

# _________________________________
## scrapy variables and relative path

# <response> variable stores scraped html content
response

# <quote> variable - stores a single block of object
quote = response.xpath('//*[@class="quote"]')[0]

# relative paths within the single block
quote.xpath('.//*[@class="text"]/text()').extract()  # a list of texts
quote.xpath('.//*[@itemprop="author"]/text()').extract()
quote.xpath('.//meta[@itemprop="keywords"]/@content').extract()

quote.xpath('.//*[@class="text"]/text()').extract_first()  # the first text
quote.xpath('.//*[@class="text"]/text()').extract()[0]  # the first text

# _________________________________
## complete URL
relative_url = response.xpath('//nav//li[@class="next"]/a/@href').extract_first()
complete_url = response.urljoin(relative_url)
