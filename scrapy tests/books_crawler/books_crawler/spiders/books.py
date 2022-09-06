## Simple scrapy test 02: class CrawkSpider
## This is to automatically extract urls all available urls accessible from the target website

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    # APIs: https://docs.scrapy.org/en/latest/topics/spiders.html
    # 1. Use callback function to parse the response (web page) and return either Item objects, Request objects, or an iterable of both
    # - I suppose the callback function can be renamed (by default: parse; here: renamed as parse_page)
    # 2. follow=False: only obtain urls in the current page; follow=True: click the obtained urls and follow the same "callback" rules
    # 3. Other rule parameters: deny_domains - ditch those urls; allow - only use urls including key works
    # - I believe scrapy automatically remove duplicate urls
    rules = (Rule(LinkExtractor(deny_domains=('google.com','facebook.com'), allow=("music")), \
    callback='parse_page', follow=True),)

    # <response> stores scrapped web content by scrapy
    # 1st: content of the initial page (could be <fetch("xx/url")> or inherited from CrawlSpider or Spider)
    # 2nd: content of another page - will overwrite the 1st response (e.g. Request("xx/another/url"))
    def parse_page(self, response):
        yield {'URL': response.url}  # 1st <response> - already inherited the <url> attribute for the current page url
