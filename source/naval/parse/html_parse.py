import mimetypes
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from ..utility import directories
from .parse_base import Parse_Base
from ..fetch.fetch_base import Fetch_Base


class HTML_Parse(Parse_Base):
    '''Parses html data from fetch object'''
    # fetch object with html data is expected
    fetch_content_type = "text/html"

    def __init__(self, fetch_obj) -> None:
        super().__init__(fetch_obj)
        # specify type of doc object(type annotation)
        self.doc = self.create_doc()

    def create_doc(self) -> BeautifulSoup:
        '''Create BeautifulSoup object for parsing HTML'''
        fetch_file = self.fetch_obj.get_file()
        fetch_file.seek(0)
        return BeautifulSoup(fetch_file, 'html.parser')

    def text_to_file(self):
        '''Parses text and store it to self.text_file'''
        self.text_file.write(self.doc.get_text())

    def html_to_file(self):
        '''Parses html and store it to self.html_file'''
        format_html = self.doc.prettify(formatter="html")
        self.html_file.write(format_html.encode(encoding="utf-8"))

    def get_title(self) -> str or bytes:
        '''Returns title tag text'''
        if self.doc.title != None:
            return self.doc.title.get_text()


    @classmethod
    def is_source_parsable(cls, source: str) -> bool:
        '''Checks if source can be parsed based on its mimetype\n
        source - file path or url'''
        # extract the path part of url
        url_path = urlparse(source).path
        # guess mimetype from the path
        fetch_type = mimetypes.guess_type(url_path)[0]
        # If its None then it may be a webpage which is mostly HTML
        # super class is also for urls with .html path or similar
        return fetch_type == None or super().is_source_parsable(source)

if __name__ == "__main__":
    from ..fetch.web_fetch import Web_Fetch

    # create fetch object
    url = "https://pdfminersix.readthedocs.io/en/latest/tutorial/highlevel.html"
    fetch_obj = Web_Fetch(url)
    # this performs request for data
    fetch_obj.request()

    # create parse object from fetch object
    parse_obj = HTML_Parse(fetch_obj)
    soup = parse_obj.doc
    parse_obj.text_to_html()
    print(len(soup.find_all()))