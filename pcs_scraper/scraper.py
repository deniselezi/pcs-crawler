from selenium import webdriver

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scraper:
    def __init__(self, headless=True):
        if headless:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=options)
        else:
            self.driver = webdriver.Chrome()

        self.md_contents = {}
        self.is_signed_in = False

    def scrape(self, url, user, password):
        """
        Given a repository URL, handles signing into GitHub and extracts
        the text contents of all markdown files in the repository.
        """
        self.driver.get(url)
        if not self.is_signed_in:
            self.__sign_in(user, password)
            self.is_signed_in = True
        self.__search_results()
        for md_url in self.__fetch_markdowns():
            self.md_contents[md_url] = self.__read_md(md_url)
        return self.md_contents

    def quit(self):
        self.driver.quit()

    def __search_results(self):
        def build_url(user, repo):
            return f"https://github.com/search?q=repo%3A{user}/{repo}%20path%3A.md&type=code"

        elems = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//a[@class='AppHeader-context-item']/span")
            )
        )
        search_results_url = build_url(elems[0].text, elems[1].text)
        self.driver.get(search_results_url)

    def __sign_in(self, user, password):
        elems = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.LINK_TEXT, "Sign in"))
        )
        sign_in_button = elems[0]
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
        try:
            elems = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//a[@data-testid='link-to-search-result']")
                )
            )
        except TimeoutException:
            # can be triggered by "Not indexed yet"
            # https://github.com/orgs/community/discussions/107482
            print("Timeout error on markdowns fetch")
            elems = []

        return [e.get_attribute("href") for e in elems]

    def __read_md(self, url):
        self.driver.get(url)

        text_area = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "read-only-cursor-text-area"))
        )

        return text_area.text
