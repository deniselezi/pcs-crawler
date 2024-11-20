import markdown
from bs4 import BeautifulSoup

def markdown_to_text(markdown_file):
    with open(markdown_file, 'r', encoding="utf-8") as f:
        markdown_content = f.read()
    html_content = markdown.markdown(markdown_content)
    soup = BeautifulSoup(html_content, 'html.parser')
    plain_text = soup.get_text()
    return html_content,plain_text

def extract_links(html_content):
    repo_links = set()
    soup = BeautifulSoup(html_content, 'html.parser')
    base_url = "https://github.com"
    for a in soup.find_all('a'):
        try:
            href = a['href']
            if href.startswith(base_url):
                slice_chars = len(base_url)
                href_sliced = href[slice_chars+1:len(href)].split("/")
                user_or_group = href_sliced[0]
                repo = href_sliced[1]
                repo_links.add(f"{base_url}/{user_or_group}/{repo}")
        except KeyError:
            continue

    print(repo_links)

html_content,plain_text = markdown_to_text('example.md')

extract_links(html_content)

with open('output.txt', 'w',encoding="utf-8" ) as output_file:
    output_file.write(plain_text)