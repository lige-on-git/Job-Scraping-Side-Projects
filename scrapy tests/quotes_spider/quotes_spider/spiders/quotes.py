## Simple scrapy test 01: class scrapy.Spider
## This is to manually extract urls to reach and extract infor from new webpages

import scrapy
class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    # <response> stores scrapped web content by scrapy
    # 1st: content of the initial page (could be <fetch("xx/url")> or inherited from CrawlSpider or Spider)
    # 2nd: content of another page - will overwrite the 1st response (e.g. Request("xx/another/url"))
    def parse(self, response):
        # This is NOT a <callback> function

        # a list of selector blocks
        quotes = response.xpath('//*[@class="quote"]')  # 1st <response>
        for quote in quotes:
            # extract text string (not list)
            text = quote.xpath('.//*[@class="text"]/text()').extract_first()
            author = quote.xpath('.//*[@itemprop="author"]/text()').extract_first()
            tags = quote.xpath('.//meta[@itemprop="keywords"]/@content').extract_first()

            # for each selector block we yield a dict (can only yield in a function - here <parse()>)
            yield {"URL":response.url,  # <response.url> stores the current page url
                   "Text":text,
                   "Author":author,
                   "Tags":tags}

        next_page_url = response.xpath('//nav//li[@class="next"]/a/@href').extract_first()

        # the current page usrl is already recorded in response.url attribute.
        # CAN'T do this if a path is "clicked" by Selenium
        # (e.g. in books_selenium <next_page.click()> - response.url doesn't exist for the "next_page")
        abs_next_page_url = response.urljoin(next_page_url)

        # request content from the next url
        yield scrapy.Request(abs_next_page_url)  # 2nd <response> now overwrite the 1st one
