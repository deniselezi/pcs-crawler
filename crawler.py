from bs4 import BeautifulSoup
from collections import deque

import math
import requests

class Crawler:
    def __init__(self, start_point, crawl_limit=None):
        self.to_crawl = deque([start_point])
        self.crawl_limit = crawl_limit if crawl_limit else math.inf
        self.crawls = 0
        self.mds = []
        self.crawl()
    

    def crawl(self):
        while self.to_crawl and self.crawls < self.crawl_limit:
            url = self.to_crawl.popleft()
            print(url)
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')

            file_tags = soup.find_all('a', class_='Link--primary')  # list of files/dirs in repo's file explorer
            file_tags = filter(lambda tag: len(tag.get('class')) == 1, file_tags)

            log = set()

            for tag in file_tags:
                if not tag.text in log:
                    if tag.get('aria-label').find('(Directory)') != -1:
                        self.to_crawl.append("https://github.com" + tag.get('href'))
                        log.add(tag.text)
                    else:  # file
                        if tag.text.endswith('.md'):
                            self.mds.append((tag.text, tag.get('href')))  # later edit to show location of file
                            log.add(tag.text)
