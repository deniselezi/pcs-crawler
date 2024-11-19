from dotenv import find_dotenv, load_dotenv
from collections import deque

from parser.parser import MarkdownParser
from scraper.scraper import Scraper

import math
import sys
import os


class Crawler:
    def __init__(self, start_point, crawl_limit=None):
        self.to_crawl = deque([start_point])
        self.crawl_limit = crawl_limit if crawl_limit else math.inf
        self.crawls = 0

        self.parser = MarkdownParser()
        self.scraper = Scraper()

    def crawl(self, user, password):
        while self.to_crawl and self.crawls < self.crawl_limit:
            url = self.to_crawl.popleft()
            md_contents = self.scraper.scrape(url, user, password)
            for key, val in md_contents.items():
                print(f"Text of markdown file at {key} url")
                print(self.parser.parse(val)[:100])
                print("\n\n\n")


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


def command_failed():
    exit()


"""Extracts arguments and validates them."""
def get_args(args):
    args.pop(0)  # remove filename
    n_args = len(args)

    if not (1 <= n_args <= 2):
        print("Invalid number of args, please follow the correct format")
        print("COMMAND: python3 pcs-crawler.py LINK [MAX_REPOS]")
        return command_failed()

    if not args[0].startswith("http"):
        print("First arg is not a valid URL")
        return command_failed()

    if n_args == 2 and not(args[1].isdigit()):
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

    url = generate_url(args)
    user, password = os.getenv("USER"), os.getenv("PASSWORD")

    if not url:
        print("Please provide an URL")
        command_failed()

    if not user or not password:
        print("Could not fetch username and/or password from .env")
        command_failed()

    crawler = Crawler(url)
    crawler.crawl(user, password)
