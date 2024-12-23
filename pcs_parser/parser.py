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
        urls = self._find_repos(text)
        html_content = markdown.markdown(text)

        soup = BeautifulSoup(html_content, "html.parser")
        text = soup.get_text()
        return text, urls

    def _find_repos(self, text):
        pattern = r"https:\/\/github\.com\/[\w\-]+\/[\w\-]+(?=\/?)"
        cleaned_repos = self._clean(set(re.findall(pattern, text)))
        return cleaned_repos

    def _clean(self, repos_obtained):
        blacklist = ["https://github.com/signup/free"]
        for blacklist_link in blacklist:
            repos_obtained.discard(blacklist_link)
        return repos_obtained
