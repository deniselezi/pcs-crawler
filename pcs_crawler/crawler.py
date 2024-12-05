from collections import deque
import os

from dotenv import find_dotenv, load_dotenv

class Crawler:
    def __init__(self, env_path, URL, CRAWL_LIMIT):
        self.URL = URL
        self.CRAWL_LIMIT = CRAWL_LIMIT
        self.env_path = env_path
        pass

    def run(self):
        # Start Crawling
        to_crawl = deque([self.URL])
    



if __name__ == "__main__":
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    user, password = os.getenv("USER"), os.getenv("PASSWORD")
    