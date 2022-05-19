from io import FileIO, IOBase

from .fetch.fetch_base import Fetch_Base
from .parse.parse_base import Parse_Base

from .fetch.fetch import Fetch
from .parse.parse import Parse

from .text.text import Text

import time

class Crawl_Base(Text):
    '''Base class for crawling through resources e.g pdf files, webpages'''

    def __init__(self, source, section_max_size=100000, **kwarg):
        '''
        source - mostly url, file path or file object.\n
        section_max_size - maximum allowed section size.\n
        **kwarg - optional arguments including metadata(dictionary) and 
        title(str) of crawled document.
        '''
        super().__init__(source, section_max_size=section_max_size, **kwarg)    
        # self._source may be different from source argument
        # source may be file object but self._source be its path
        self.crawl(source)

    def get_fetch(self, source: str or IOBase) -> Fetch_Base:
        '''Returns parse object for fetch object'''
        # Fetch class is created from composition of another parse object
        # And inheritance of Fetch_Base to give fetch object like behaviour
        # use Fetch().get_fetch() to get underlying fetch object
        return Fetch(source)

    def get_parse(self, fetch_obj: Fetch_Base) -> Parse_Base:
        '''Returns parse object for fetch object'''
        # Parse object is created from composition of another parse object
        # And inheritance of Parse_Base to give parse object like behaviour
        # use Parse().get_parse() to get underlying parse object
        return Parse(fetch_obj)

    def crawl(self, source):
        '''Fetch and parse data from source creating list of sections'''
        # create fetch object
        fetch_obj = self.get_fetch(source)
        parse_obj = self.get_parse(fetch_obj)
        self.sections = self.create_sections(parse_obj.get_text(), 
        self.section_max_size)


if __name__ == "__main__":
    crawl_obj = Crawl_Base("https://www.example.com/not_found.htm")
    # print the last section object
    print(crawl_obj[-1])
