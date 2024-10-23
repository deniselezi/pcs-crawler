from crawler import Crawler


search_results_url = "https://github.com/search?q=repo%3ASpoonLabs/astor%20path%3A.MD&type=code"

crawler = Crawler(search_results_url)
crawler.crawl()
