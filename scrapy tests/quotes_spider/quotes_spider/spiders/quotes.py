import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # a list of selector blocks
        quotes = response.xpath('//*[@class="quote"]')
        for quote in quotes:
            # extract text string (not list)
            text = quote.xpath('.//*[@class="text"]/text()').extract_first()
            author = quote.xpath('.//*[@itemprop="author"]/text()').extract_first()
            tags = quote.xpath('.//meta[@itemprop="keywords"]/@content').extract_first()

            # for each selector block we yield a dict
            yield {"Text":text,
                   "Author":author,
                   "Tags":tags}

        next_page_url = response.xpath('//nav//li[@class="next"]/a/@href').extract_first()
        abs_next_page_url = response.urljoin(next_page_url)

        # request content from the next url
        yield scrapy.Request(abs_next_page_url)
