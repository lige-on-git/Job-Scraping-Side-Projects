## Simple scrapy test 03:
## Use Scrapy-Selenium to crawl and scrap the books website
## To install selenium - $ pip install selenium
## To download webdriver of chrome - https://chromedriver.chromium.org/downloads

from selenium import webdriver
from scrapy.selector import Selector
import scrapy

from time import sleep
from selenium.common.exceptions import NoSuchElementException

class BooksSpider(scrapy.Spider):
    name = 'books-selenium'
    allowed_domains = ['books.toscrape.com']

    def start_requests(self):
        self.driver = webdriver.Chrome('../../chromedriver_linux64/chromedriver')  # point to web driver
        self.driver.get("https://books.toscrape.com/index.html")  # get web content (via driver rather than response)

        sel = Selector(text=self.driver.page_source)  # convert to selector (now <sel> serves the same role as <response>)
        book_urls = sel.xpath('//h3/a/@href').extract()

        for book in book_urls:
            self.full_url = "https://books.toscrape.com/" + book

            ## A - request content from the book url - to parse info of each book
            yield scrapy.Request(self.full_url, callback=self.parse_book)

        while True:
            ## B - go the the next page (by clicking 'url' through selenium)
            try:
                next_page = self.driver.find_element("xpath",'//a[text()="next"]')  # use selenium to find an element
                sleep(3)  # selenium is pretty slow - give time to load
                self.logger.info("Sleeping for 3 seconds")
                next_page.click()  # click url to the next page

                ## C - recursively request content from book urls for future pages
                sel = Selector(text=self.driver.page_source)
                book_urls = sel.xpath('//h3/a/@href').extract()
                for book in book_urls:
                    self.full_url = "https://books.toscrape.com/catalogue/" + book
                    yield scrapy.Request(self.full_url, callback=self.parse_book)

            except NoSuchElementException:
                self.logger.info("No more pages to load.")
                self.driver.quit()
                break

    # <response> stores scrapped web content by scrapy
    # 1st: content of the initial page in the parse() function (could be <fetch("xx/url")> or inherited from CrawlSpider or Spider)
    # 2nd: content of another page
    # - either no callback: will overwrite the 1st response in the parse() function (e.g. Request("xx/next/page/url"))
    # - or has callback: will pass the response to the callback function like parse_book()
    def parse_book(self, response):
        # This is a <callback> function

        # Since we use selenium to access web content here, "self" might play the role of the 1st <response> (hence response.url doesn't work)
        # However, the "self" method might cause some mismatches with the 2nd "response" (e.g. "self.full_url" and "response.xpath('//h1/text()')" don't match)
        # We can still use the 2nd <response> - since we "Request" this callback function in start_requests()

        yield {"Name": response.xpath('//h1/text()').extract(),   # 2nd
               "Price": response.xpath('//div[@class="col-sm-6 product_main"]/p[@class="price_color"]/text()').extract()}
