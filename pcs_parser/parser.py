import re
import markdown
from bs4 import BeautifulSoup


class MarkdownParser:
    def __init__(self):
        pass

    def parse(self, text):
        """
        Parses markdown text into plain text.

        Args:
            text - the markdown text to convert into plain text

        Returns:
            the plain text
        """

        # Convert markdown to HTML
        html_content = markdown.markdown(text)

        # Parse the HTML and extract plain text
        soup = BeautifulSoup(html_content, "html.parser")
        text = soup.get_text()
        return text

    # Finds repos within the plaintext file to continue crawling

    def find_repos(self, text):
        pattern = r"https:\/\/github\.com\/[\w\-]+\/[\w\-]+(?=\/?)"
        return set(re.findall(pattern, text))

    def clean(self, repos_obtained):
        blacklist = ["https://github.com/signup/free"]
        for blacklist_link in blacklist:
            repos_obtained.discard(blacklist_link)
        return repos_obtained
