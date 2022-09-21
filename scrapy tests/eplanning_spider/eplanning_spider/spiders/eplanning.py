# Comprehensive scrapy project 01:
# Uses scrapy to crawl and scrap a java-script equipped dynamic website.
# Uses form requests to interact with the website.
# Layers multiple callback functions to access and parse each target.

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
        # This is another <callback> function
        application_urls = response.xpath('//table//td/a/@href').extract()
        for url in application_urls:
            url = response.urljoin(url)
            yield scrapy.Request(url, callback=self.parse_items)  # pass the response of application info to another content parser

        # go to a new result page
        next_page_url = response.xpath('//*[@rel="next"]/@href').extract_first()
        next_page_url = response.urljoin(next_page_url)
        if len(next_page_url) != 0:  # pass the next result page to this callback function itself until reaching the last page
            yield scrapy.Request(next_page_url, callback=self.parse_pages)

    def parse_items(self, response):
        # This is another <callback> function
        # if click "Agent" button, javascript will run to display the agent table.
        # however, the agent table is already embeded in the html file so no form request needed
        response.xpath('//*[@value="Agents"]/@style').extract_first()

        'display: inline;  visibility: visible;'

        agent_name = response.xpath('//tr[th="Name :"]/td/text()').extract_first()
        if agent_name is not None:  # before process string, first make sure the output text is not None
            agent_name = agent_name.strip()

        phone = response.xpath('//tr[th="Phone :"]/td/text()').extract_first()
        if phone is not None:
            phone =  phone.strip()

        email = response.xpath('//tr[th="Email :"]/td/text()').extract_first()
        if email is not None:
            email =  email.strip()

        # address is tricky (3 lines in a table): can inspect "https://www.eplanning.ie/CarlowCC/AppFileRefDetails/22261/0"
        address_1 = response.xpath('//tr[th="Address :"]/td/text()').extract()
        address_2 = response.xpath('//tr[th="Address :"]/following-sibling::tr/td/text()').extract()[0:3]
        address = address_1 + address_2  # ccombine 2 lists

        agent_url = response.url

        yield {"name": agent_name,
               "phone": phone,
               "email": email,
               "address": address,
               "url": agent_url}
