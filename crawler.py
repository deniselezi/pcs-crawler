from collections import deque
import math
import sys
import os

from dotenv import find_dotenv, load_dotenv

from pcs_cli.cli import CLI
from pcs_parser.parser import MarkdownParser
from pcs_scraper.scraper import Scraper
from pcs_spellchecker.spellchecker import Spellchecker


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


if __name__ == "__main__":
    cli = CLI()
    args = cli.get_args(sys.argv)

    URL = args[0]
    user, password = os.getenv("USER"), os.getenv("PASSWORD")

    if not URL:
        cli.command_failed("Please provide an URL")

    if not user or not password:
        cli.command_failed("Could not fetch username and/or password from .env")

    # start crawling
    to_crawl = deque([URL])
    history = set()
    CRAWL_LIMIT = math.inf if len(args) == 1 else int(args[1])
    print(CRAWL_LIMIT)
    parser = MarkdownParser()
    scraper = Scraper(headless=False)
    spellchecker = Spellchecker()

    CRAWLS = 0
    while to_crawl and CRAWLS < CRAWL_LIMIT:
        repo_misspells = (
            {}
        )  # dict mapping repo url to a list of misspellt words and suggested fixes
        url = to_crawl.popleft()
        if url in history:
            continue
        history.add(url)
        md_contents = scraper.scrape(url, user, password)
        for key, val in md_contents.items():
            text, github_urls = parser.parse(val)
            repo_misspells[key] = spellchecker.check(text)  # possible bottleneck
            for r in github_urls:
                to_crawl.append(r)

        # serialize repo_misspells somewhere over here

        CRAWLS += 1

    # here, read previously serialized information and use it to generate the report

    scraper.quit()
