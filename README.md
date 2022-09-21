# Job-Scraping-Side-Projects
Simple side projects to practice web scraping and its connection with a database. Eventually in the main job matching project, I plan to automate job scraping from some main-stream job searching websites; maintain one relational database to store pre-processed and raw data; provide back end API for teammates to do job matching modelling.

If time permits, may also wrap up other teammates' code (quite unfortunate that not many science students write production code and use git to collaborate with others).

Side projects list:

1. In '/quotes_spider', there is simple scrapy test 01 (to manually extract urls to reach and extract info from new webpages.

2. In '/books_crawler', there is simple scrapy test 02 (to automatically extract all available urls accessible from the target website)

3. In '/selenium_test', there is simple scrapy test 03 (use Scrapy-Selenium to crawl and scrap the books website). Used callback function to parse each individual book.

4. In '/selenium_test', there is simple scrapy test 04 (use Scrapy-only to crawl and scrap the books website). Used callback function to parse each individual book.

5. In '/eplanning_spider', there is a more comprehensive web scrapping project which uses scrapy to crawl and scrap a java-script equipped dynamic website. Form requests are used to interact with the target website. Multiple callback functions are layered together to access and parse each available application.

6. (Linkedin profile scrapping)
4.2 (add database support to bookstore project)

7. (Lindedin job scrapping)


There are also two command summary files (will actively update):

1. 'scrapy_bash_commands.sh': how to start a scrapy project and run scrapy scripts in shell commands.

2. 'scrapy_shell_commands.py': how to do basic tests in scrapy shell.
