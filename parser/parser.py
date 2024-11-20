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
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        return text
    
    def extract_links(self,link):
        # Extract github links from plaintext file

        

        pass


