# Comprehensive scrapy project:
# Uses scrapy to crawl and scrap a java-script equipped dynamic website.
# Uses form requests to interact with the website.
# Layers multiple callback functions to access and parse each target

import scrapy
class EplanningSpider(scrapy.Spider):
    name = 'eplanning'
    allowed_domains = ['eplanning.ie']
    start_urls = ['http://eplanning.ie/']

    def parse(self, response):
        # This is NOT a <callback> function, just do initial search from the start_urls
        initial_urls = response.xpath('//td/a/@href').extract()
        for url in initial_urls:
            if '#' == url:  # filter out invalid urls
                pass
            else:  # request a new url, and send the response to parse_application()
                yield scrapy.Request(url, callback=self.parse_application)

    def parse_application(self, response):
        # This is a <callback> function
        # request a new url, and send the response to parse_form()
        app_url = response.xpath('//*[contains(text(), "Received")]/@href').extract_first()
        yield scrapy.Request(response.urljoin(app_url), callback=self.parse_form)

    def parse_form(self, response):
        # This is another <callback> function
        # check: https://www.eplanning.ie/CavanCC/SearchListing/RECEIVED
        # the "search" button has no attached URL in the HTML file, so can't use scrapy.Request() to "GET" a new page response.
        # instead, we use scrapy.FormRequest() to "POST" (create new) a new form (stored in tag <form></form>)
        # To check form data: Inspect -> Network (then click "search") -> searchresults -> Payload -> Form Data
        yield scrapy.FormRequest.from_response(response,
              formdata={'RdoTimeLimit': '42'},
              dont_filter=True,  # search result url is reused for all searches - so disable the scrapy default same-url filter
              formxpath='(//*[@class="container body-content"]/form)',  # can have multiple forms, must find the correct path
              callback=self.parse_pages)

    def parse_pages(self, response):
        pass
