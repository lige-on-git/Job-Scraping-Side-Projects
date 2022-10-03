# selenium wait: https://selenium-python.readthedocs.io/waits.html
# 1. -time.sleep() - pauses code execution for an exact amount of time.
# 2. -implicit wait - declared globally, tells web driver to wait for certain amount of time before any
#   driver.find_element() functions throwing a "NoSuchElementException".
#   may not wait the maximum amount of time if an element are found earlier.
# 3. -explicit wait - wait until a certain condition to occur before proceeding further in the code.
#   throw "TimeoutException" if the condition does not occur when the maximum amount of time is reached.
#   may not wait the maximum amount of time if the condition is reached earlier

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import random
from time import sleep
import csv

credential_path = '../../../login-credentials.csv'
driver_path = '../../chromedriver_linux64/version_105/chromedriver'
linkedin_home = 'https://www.linkedin.com/'

with open(credential_path, 'r') as file:
    credentials = list(csv.reader(file))  # convert iterable to list
    email = credentials[0][1]
    password = credentials[1][1]

def short_sleep():
    # customize random sleeping time
    sleep(round(random.uniform(0.8, 4.2),2))

def long_sleep():
    # customize random sleeping time
    sleep(round(random.uniform(4.2, 12.7),2))

def login_module():
    ## log-in module of linkedin using selenium (with many educational comments and redundant lines)

    # initialize driver in detach mode - keep browser open after finishing all the tasks
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(driver_path, chrome_options=chrome_options)  # add option to driver
    driver.maximize_window()

    driver.get(linkedin_home)
    short_sleep()

    # declare globle implicit wait
    driver.implicitly_wait(round(random.uniform(2.3, 3.6),2))

    try:
        # xpath objects wrapped in both <a> (contains a url) and <button> (contains no url - javascript driven) tags are clickable
        driver.find_element("xpath",'//button[contains(text(), "Sign in")]') # find_element() will only return the first element
        driver.find_elements("xpath",'//*[contains(text(), "Sign in")]')  # driver.find_elements() will return all eligible elements

        driver.find_element("xpath",'//a[contains(text(), "Sign in")]').click()
        long_sleep()

        # selenium can not only find elements by xpath, can also use attribute names.
        # the two commands immediately below both return the same username input element wrapped in <input> tags.
        # there is also an outter <form> tag - so can use scrapy form request too (but hard to bypass robot check)
        driver.find_element("name", 'session_key')
        username_input = driver.find_element("id", 'username')
        username_input.send_keys(email)  # use selenium to send input to fill the form
        long_sleep()

        password_input = driver.find_element("id", 'password')
        password_input.send_keys(password)  # never ever put actual password in code and upload to github....
        short_sleep()

        driver.find_element("xpath",'//button[contains(text(), "Sign in")]').click()

        # after using the login module, manually check if successful and then continue
        print('Press Enter to continue:')
        input()

    except NoSuchElementException:
        print("Cannot find sign-in button in at least one occasion")
        driver.quit()


if __name__ == "__main__":
    # the following code get executed when run this file directly (good for testing purpose)
    login_module()

else:
    # the following code get executed when this file is imported
    pass
