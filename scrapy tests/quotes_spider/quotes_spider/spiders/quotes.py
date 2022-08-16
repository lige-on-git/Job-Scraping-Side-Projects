import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        h1_tag = response.xpath('//h1/a/text()').extract()[0]
        pop_tags = response.xpath('//*[@class="tag-item"]/a/text()').extract()

        yield {"H1 Tag":h1_tag, "Popular Tags":pop_tags}
