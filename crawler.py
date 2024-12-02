from collections import deque
import math
import sys
import os

from dotenv import find_dotenv, load_dotenv

from pcs_parser.parser import MarkdownParser
from pcs_scraper.scraper import Scraper
from pcs_spellchecker.spellchecker import Spellchecker


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


def _check_type(expected_type, args):
    return all(isinstance(item, expected_type) for item in args)


def command_failed():
    print("COMMAND: python3 pcs-crawler.py LINK [MAX_REPOS]")
    sys.exit(1)


def get_args(args):
    """Extracts arguments and validates them."""
    args.pop(0)  # remove filename
    n_args = len(args)

    if not _check_type(str, args):
        print("Arguments aren't all strings.")
        return command_failed()

    if not 1 <= n_args <= 2:
        print("Invalid number of args, please follow the correct format")
        return command_failed()

    if not args[0].startswith("https://github.com/"):
        print("First arg is not a valid GitHub URL")
        return command_failed()

    if n_args == 2 and not args[1].isdigit():
        print("Incorrect command usage, argument 2 is not an integer")
        return command_failed()

    return args


if __name__ == "__main__":
    args = get_args(sys.argv)

    URL = args[0]
    user, password = os.getenv("USER"), os.getenv("PASSWORD")

    if not URL:
        print("Please provide an URL")
        command_failed()

    if not user or not password:
        print("Could not fetch username and/or password from .env")
        command_failed()

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
