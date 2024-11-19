from selenium import webdriver

# from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome()  # or any other Selenium driver
        self.md_contents = {}

    def scrape(self, url, user, password):
        """
        Given a repository URL, handles signing into GitHub and extracts
        the text contents of all markdown files in the repository.
        """

        # try:
        #     self.driver.get(url)
        #     self.__sign_in(user, password)

        #     for md_url in self.__fetch_markdowns():
        #         self.md_contents[md_url] = self.__read_md(md_url)

        # except TimeoutException:

        self.driver.get(url)
        self.__sign_in(user, password)

        for md_url in self.__fetch_markdowns():
            self.md_contents[md_url] = self.__read_md(md_url)
        return self.md_contents

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

        return [e.get_attribute("href") for e in elems]

    def __read_md(self, url):
        self.driver.get(url)

        text_area = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "read-only-cursor-text-area"))
        )

        return text_area.text
