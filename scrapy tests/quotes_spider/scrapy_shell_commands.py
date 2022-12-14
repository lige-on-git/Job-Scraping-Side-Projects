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
## complete URL (also works for all relative urls even like this "../../new_address")
relative_url = response.xpath('//nav//li[@class="next"]/a/@href').extract_first()
complete_url = response.urljoin(relative_url)

# _________________________________
## contents contained in an attribute
# (e.g. get the full content that contains sub-string "star" in a class attribute)
fetch("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
response.xpath('//*[contains(@class, "star")]/@class').extract()
response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
# response.xpath('//*[contains(text(), "Received")]')  # can even be used for text()

# _________________________________
## the next tag (not nested) (e.g. a stand-alone <p> is difficult to locate by itself)
fetch("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
response.xpath('//*[@id="product_description"]/following-sibling::p/text()').extract()  # only return the next p tag
response.xpath('//*[@id="product_description"]/following::p/text()').extract_first()  # a list of all following p

## can also identify using [contains()], [@id='xxx'], and even [text()='xxx'] to help locate
fetch("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
response.xpath("//th[text()='UPC']/text()").extract_first()
response.xpath("//th[text()='UPC']/following-sibling::td/text()").extract_first()

# _________________________________
## tune form (https://docs.scrapy.org/en/latest/topics/request-response.html)
fetch('https://www.eplanning.ie/CarlowCC/SearchListing/RECEIVED')
response.url
len(response.xpath('//form'))  # to check how many form tags in this html file
form = scrapy.FormRequest.from_response(response,
       formdata={'RdoTimeLimit': '42'},  # override the default form data
       formxpath='(//*[@class="container body-content"]/form)')  # locate the correct <form> tag can be time consuming
fetch(form)
response.url  # get https://www.eplanning.ie/CavanCC/searchresults, which is not unique (can try this url without requesting form)
view(response)  # view response in a browser


# _________________________________
fetch('https://www.eplanning.ie/CarlowCC/AppFileRefDetails/22261/0')
## control level of a selector

# two nested tags <tr> and <th>, where text() wrapped in <tr> tag is "Name :"
# 1. locate <tr> selector using info of its child tag <th>, while selector remains on the level of <tr>
response.xpath('//tr[th="Name :"]')

# this is important if we need to access sibling tags of the upper tag <tr> (can otherwise be tricky)
response.xpath('//tr[th="Name :"]/following-sibling::tr/th/text()').extract()

# 2. In contrast, this will only locate selector on the level of <th> (less useful in the previous example)
response.xpath('//tr/th[text()="Name :"]')
