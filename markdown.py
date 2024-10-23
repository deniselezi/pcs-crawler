import markdown
from bs4 import BeautifulSoup

def markdown_to_text(markdown_file):
    # Read the markdown file
    with open(markdown_file, 'r', encoding="utf-8") as f:
        markdown_content = f.read()

    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_content)

    # Parse the HTML and extract plain text
    soup = BeautifulSoup(html_content, 'html.parser')
    plain_text = soup.get_text()

    return plain_text

# Example usage
plain_text = markdown_to_text('example.md')
print(plain_text)

# Optionally save the plain text to a file
with open('output.txt', 'w',encoding="utf-8" ) as output_file:
    output_file.write(plain_text)