from collections import deque

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import math
import time


class Crawler:
    def __init__(self, start_point, crawl_limit=None):
        self.to_crawl = deque([start_point])
        self.crawl_limit = crawl_limit if crawl_limit else math.inf
        self.crawls = 0
        self.mds = []

        self.driver = webdriver.Chrome()  # or any other Selenium driver

    def crawl(self, user, password):
        while self.to_crawl and self.crawls < self.crawl_limit:
            url = self.to_crawl.popleft()
            self.driver.get(url)

            self._sign_in(user, password)

    def _sign_in(self, user, password):
        elems = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "types__StyledButton-sc-ws60qy-0")
            )
        )

        sign_in_button = next(filter(lambda a: a.text == "Sign in", elems))
        sign_in_button.click()

        username_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "login_field"))
        )
        password_input = self.driver.find_element(By.ID, "password")
        username_input.send_keys(user)
        password_input.send_keys(password)

        sign_in_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        sign_in_button.click()
        time.sleep(3)
