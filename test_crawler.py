from crawler import Crawler


search_results_url = "https://github.com/SpoonLabs/astor"

crawler = Crawler(search_results_url)
crawler.crawl()
