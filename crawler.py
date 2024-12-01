from collections import deque
import math
import sys
import os
import re

from dotenv import find_dotenv, load_dotenv

from pcs_parser.parser import MarkdownParser
from pcs_scraper.scraper import Scraper


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


def _check_type(expected_type, args):
    return all(isinstance(item, expected_type) for item in args)


def _is_repo_url(url):
    pattern = r"https:\/\/github\.com\/[\w\-]+\/[\w\-]+(?=\/?)"
    if re.search(pattern,url):
        print("Found a match?")
        return True
    else:
        return False


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

    if not args[0].startswith("http"):
        print("First arg is not a valid URL")
        return command_failed()

    if n_args == 2 and not args[1].isdigit():
        print("Incorrect command usage, argument 2 is not an integer")
        return command_failed()

    return args


def generate_url(args):
    repo_link = args[0].split("/")[-2:]

    group_name, repo_name = repo_link[0], repo_link[1]

    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    url = f"https://github.com/search?q=repo%3A{group_name}/{repo_name}%20path%3A.md&type=code"
    return url


if __name__ == "__main__":
    args = get_args(sys.argv)

    URL = generate_url(args)
    user, password = os.getenv("USER"), os.getenv("PASSWORD")

    if not URL:
        print("Please provide an URL")
        command_failed()

    if not user or not password:
        print("Could not fetch username and/or password from .env")
        command_failed()

    # start crawling

    to_crawl = deque([URL])
    CRAWL_LIMIT = int(math.inf if len(args) == 1 else args[1])
    parser = MarkdownParser()
    scraper = Scraper()

    CRAWLS = 0
    while to_crawl and CRAWLS < CRAWL_LIMIT:
        url = to_crawl.popleft()
        md_contents = scraper.scrape(url, user, password)
        all_repos = set()
        for key, val in md_contents.items():
            print(f"Text of markdown file at {key} url")
            TEXT = parser.parse(val)
            repos = parser.find_repos(val)
            all_repos.update(repos)
            print("\n\n\n")

            # after parsing urls from markdowns, append to to_crawl here
            # to continue crawling
        CRAWLS += 1
