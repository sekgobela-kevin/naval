from io import FileIO
from .text.text import Text
from .fetch.master_fetch import Master_Fetch
from .fetch.fetch_base import Fetch_Base

import time

class Crawl_Base(Text):
    '''Base class for crawling through resources e.g pdf files, webpages'''

    def __init__(self, source, section_max_size=100000, **kwarg):
        '''
        source - mostly url, file path or file object.
        section_max_size - maximum allowed section size\n
        '''
        super().__init__(source, section_max_size=section_max_size, **kwarg)
        # pass original source as new_source may not always point to data
        # file fetch class do accept file object
        self.fetch_obj = Master_Fetch.get_fetch_object(source)
        self.crawled = False
        self.fail = False
        self.status = 0

    def is_crawled(self) -> bool:
        '''Checks if resource was crawled'''
        return self.crawled

    def parse(self, fetch_obj: Fetch_Base) -> list or str or None:
        '''Parses fetch object into text or section objects\
        fetch_obj - any object created from subclass of Fetch_Base.
        Contains get_file() which returns file with fetched data'''
        raise NotImplementedError()  

    def request(self, attempts=2, attempt_inteval=1) -> list:
        '''Crawls for data in source and setup resource\n
        attempt [int] - how may times to retry crawling if fails\n
        attempt_inteval [number] - time in seconds to before retrying'''
        if not isinstance(attempts, (int)):
            raise TypeError("attempt should be integer not ", type(attempts))
        if not isinstance(attempt_inteval, (int, float)):
            raise TypeError("attempt_inteval should be a number(float, int) not ",
            type(attempts))
        if not Master_Fetch.is_source_valid(self._source):
            raise Exception(f"source ({self._source}) is invalid")
        # this store results of crawling
        parse_output = None
        # try crawling for value in attempt
        for attempt in range(attempts):
            # check if source is active(e.g file available)
            if Master_Fetch.is_source_active(self._source):
                # fetch data from self._source if not fetched
                self.fetch_obj.request()
                # parse fetched data if available
                parse_output = self.parse(self.fetch_obj)
                self.crawled = True
                # update to show that crawl passed/successful
                if parse_output != None:
                    self.status = 200
            # update to show that source was crawled
            self.crawled = True
            # dont retry if crawl succeeded
            if self.status == 200:
                break
            # sleep before retrying to crawl again
            time.sleep(attempt_inteval)
        if isinstance(parse_output, str):
            # create sections from returned string
            print(self.section_max_size)
            self.sections = self.create_sections(parse_output, 
            self.section_max_size)
        elif isinstance(parse_output, list):
            # initialise section objects from returned section objects
            self.sections = parse_output
        elif parse_output == None:
            # crawling failed to return data
            self.status = 1000
            self.failed = True
        else:
            # theres problem with output of crawl(self, source)
            raise Exception(f"parse_output should be list, str,\
            or None not", type(parse_output))
        return self.sections.copy()



if __name__ == "__main__":
    import os, sys

    crawl_obj = Crawl_Base(__file__, section_max_size=200)
    # read the current source file(this module)
    module_folder = os.path.dirname(__file__)
    text = open(os.path.join(module_folder, "crawl_base.py"), "r").read()
    # create section objects
    sections = crawl_obj.create_sections(text, 400)
    # add section objects
    crawl_obj.set_sections(sections)
    # print the last section object
    print(crawl_obj[-1])
