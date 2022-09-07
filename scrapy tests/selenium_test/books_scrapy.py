## Simple scrapy test 04:
## Use Scrapy-only to crawl and scrap the books website

import scrapy
class BooksSpider(scrapy.Spider):
    name = 'books-scrapy'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):
        # This is NOT a <callback> function
        book_urls = response.xpath("//h3/a/@href").extract()  # a list - all extracted urls
        for book in book_urls:
            abs_url = response.urljoin(book)

            # the "2nd" response from the new book url - then callback a function to parse book content
            # this response will ONLY be passed to the callback function
            yield scrapy.Request(abs_url, callback=self.parse_book)

        next_page_url = response.xpath("//a[text()='next']/@href").extract_first()  # a string - a single url
        abs_next_page_url = response.urljoin(next_page_url)

        # the "2nd" response from the next page url
        # this response will OVERWRITE the "1st" response in this parse() function
        yield scrapy.Request(abs_next_page_url)

    def parse_book(self, response):  # only receive requested response if this function is called back
        # This is a <callback> function
        title = response.xpath('//h1/text()').extract_first()
        price =  response.xpath('//*[@class="price_color"]/text()').extract_first()
        image_url = response.urljoin(response.xpath('//img/@src').extract_first())

        rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
        rating = rating.replace('star-rating ', '')  # full extract content example: "star-rating Three"

        description = response.xpath('//*[@id="product_description"]/following-sibling::p/text()').extract_first()

        ## to parse a table: all rows share a similar xpath - so define a inner function
        def product_info_row(name):
            return response.xpath("//th[text()='" + name + "']/following-sibling::td/text()").extract_first()

        upc = product_info_row("UPC")
        product_type = product_info_row("Product Type")
        availability = product_info_row("Availability")
        review_numbers = product_info_row("Number of reviews")

        yield {'title':title,
               'price':price,
               'image_url':image_url,
               'rating':rating,
               'description':description,
               'upc':upc,
               'product type':product_type,
               'availability': availability,
               'review numbers':review_numbers}
