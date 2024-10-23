from collections import deque

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from parser.parser import MarkdownParser

import math
import time


class Crawler:
    def __init__(self, start_point, crawl_limit=None):
        self.to_crawl = deque([start_point])
        self.crawl_limit = crawl_limit if crawl_limit else math.inf
        self.crawls = 0

        self.driver = webdriver.Chrome()  # or any other Selenium driver

    def crawl(self, user, password):
        while self.to_crawl and self.crawls < self.crawl_limit:
            url = self.to_crawl.popleft()
            self.driver.get(url)
            self.__sign_in(user, password)
            
            md_parser = MarkdownParser()
            mds = self.__fetch_markdowns()
            for md_url in mds:
                md_text = self.__read_md(md_url)
                print(md_parser.parse(md_text))
                # log output somewhere here to later add onto report
                # maybe move this code out of crawler to main file

    def __sign_in(self, user, password):
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
    
    def __fetch_markdowns(self):
        elems = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//a[@data-testid='link-to-search-result']")
            )
        )

        return [e.get_attribute('href') for e in elems]

    def __read_md(self, url):
        self.driver.get(url)

        text_area = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "read-only-cursor-text-area"))
        )

        return text_area.text

