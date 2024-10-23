from collections import deque

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

import math
import time


class Crawler:
    def __init__(self, start_point, crawl_limit=None):
        self.to_crawl = deque([start_point])
        self.crawl_limit = crawl_limit if crawl_limit else math.inf
        self.crawls = 0
        self.mds = []

        self.driver = webdriver.Chrome()  # or any other Selenium driver

        self.crawl()

    def crawl(self):
        while self.to_crawl and self.crawls < self.crawl_limit:
            url = self.to_crawl.popleft()
            self.driver.get(url)

            self._sign_in()

    def _sign_in(self):
        elems = self.driver.find_elements(
            By.CLASS_NAME, "types__StyledButton-sc-ws60qy-0"
        )
        sign_in_button = next(filter(lambda a: a.text == "Sign in", elems))
        
        sign_in_button.click()
        time.sleep(3)

        username_input = self.driver.find_element(
            By.ID, "login_field"
        )

        password_input = self.driver.find_element(
            By.ID, "password"
        )

        # print(username_input)
        # print(password_input)

        username_input.send_keys("username")
        time.sleep(1)
        password_input.send_keys("password")
        time.sleep(1)
        
        sign_in_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        print(sign_in_button)
        sign_in_button.click()
        time.sleep(3)

        # for l in login:
        #     print(l.text)

# "types__StyledButton-sc-ws60qy-0 
# 