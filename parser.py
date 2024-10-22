import requests
from bs4 import BeautifulSoup


search_results_url = "https://github.com/search?q=repo%3ASpoonLabs/astor%20path%3A.md&type=code"

page = requests.get(search_results_url)

soup = BeautifulSoup(page.text, 'html.parser')

a_tags = soup.find_all('a')

links = [tag.get('href') for tag in a_tags]

title = soup.find('title')

# print(title)

# print(links)

for l in links:
    if l.find("blob") != -1:
        print(l)

print(soup.prettify()[:50000])
