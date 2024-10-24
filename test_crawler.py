import os

from crawler.crawler import Crawler
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path, override=True)

search_results_url = (
    "https://github.com/search?q=repo%3ASpoonLabs/astor%20path%3A.MD&type=code"
)

print(os.getenv("USER"))

crawler = Crawler(search_results_url)
crawler.crawl(os.getenv("USER"), os.getenv("PASSWORD"))
