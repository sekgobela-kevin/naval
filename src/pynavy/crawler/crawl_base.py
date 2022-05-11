from io import FileIO

from .text.text import Text
from .fetch.master_fetch import Master_Fetch
from .parse.master_parse import Master_Parse

import time

class Crawl_Base(Text):
    '''Base class for crawling through resources e.g pdf files, webpages'''

    def __init__(self, source, section_max_size=100000, **kwarg):
        '''
        source - mostly url, file path or file object.
        section_max_size - maximum allowed section size\n
        '''
        super().__init__(source, section_max_size=section_max_size, **kwarg)
        # create fetch object
        fetch_obj = Master_Fetch.get_fetch_object(source)
        parse_obj = Master_Parse.get_parse_object(fetch_obj)
        self.sections = self.create_sections(parse_obj.get_text(), 
        section_max_size)


if __name__ == "__main__":
    import os, sys

    crawl_obj = Crawl_Base(__file__, section_max_size=200)
    # print the last section object
    print(crawl_obj[-1])
