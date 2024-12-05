from collections import deque
import sys
import math
import os

from dotenv import find_dotenv, load_dotenv

from pcs_cli.cli import CLI
from pcs_parser.parser import MarkdownParser
from pcs_scraper.scraper import Scraper
from pcs_spellchecker.spellchecker import Spellchecker


class Crawler:
    def __init__(self, cli, url, crawl_limit):
        self.url = url
        self.crawl_limit = crawl_limit
        self.history = set()
        self.to_crawl = deque([url])
        self.cli = cli
        self.scraper = Scraper(headless=False)
        

    def _get_env_variables(self, key):
        value = os.getenv(key)

        if not value:
            self.cli.command_failed("Could not fetch {key} from .env")

        return value

    def start(self):
        user = self._get_env_variables("USER")
        password = self._get_env_variables("PASSWORD")


        parser = MarkdownParser()
        spellchecker = Spellchecker()

        crawls = 0

        while self.to_crawl and crawls < self.crawl_limit:
            repo_misspells = (
                {}
            )  # dict mapping repo url to a list of misspellt words and suggested fixes
            url = self.to_crawl.popleft()
            if url in self.history:
                continue
            self.history.add(url)
            md_contents = self.scraper.scrape(url, user, password)
            for key, val in md_contents.items():
                text, github_urls = parser.parse(val)
                breakpoint()

                repo_misspells[key] = spellchecker.check(
                    text
                )  # possible bottleneck
                for r in github_urls:
                    self.to_crawl.append(r)

            # serialize repo_misspells somewhere over here

            crawls += 1

            # here, read previously serialized information and use it to generate the report

        self.stop()

    def stop(self):
        self.scraper.quit()


if __name__ == "__main__":
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)

    cli = CLI()
    args = cli.get_args(sys.argv)

    URL = args[0]

    if not URL:
        cli.command_failed("Please provide an URL")

    CRAWL_LIMIT = math.inf if len(args) == 1 else int(args[1])

    crawler = Crawler(cli, URL, CRAWL_LIMIT)
    crawler.start()
