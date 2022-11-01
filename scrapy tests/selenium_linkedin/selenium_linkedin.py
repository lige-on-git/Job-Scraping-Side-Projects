## Comprehensive scrapy-selenium eproject 02:
## Use scrapy-selenium to crawl and scrap Linkedin profiles
## Linkedin is heavily java-script equipped and has robot checks, so better to use selenium with scrapy

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import random
from time import sleep

# for explicit wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from linkedin_login import *

# may use "presence_of_element_located" to continue code after manually solving robot check
element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(("xpath", '//a[contains(text(), "Sign in")]')))
element.click();
