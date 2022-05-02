from unicodedata import numeric
from text.text import Text
import time

class Crawl_Base(Text):
    '''Base class for crawling through resources e.g pdf files, webpages'''

    def __init__(self, *args):
        super().__init__(*args)
        self.crawled = False
        self.fail = False
        self.status = 0

    def is_source_valid(self, source) -> bool:
        '''Checks if source is valid'''
        raise NotImplementedError()

    def is_source_active(self, source) -> bool:
        '''Checks if data in source is accessible'''
        raise NotImplementedError()

    def is_crawled(self) -> bool:
        '''Checks if resource was crawled'''
        return self.crawled

    def crawl(self, source) -> list or str or None:
        '''Crawls through a resource and returns text or section objects'''
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
        if self.is_source_valid(self._source):
            raise Exception(f"source ({self._source}) is invalid")
        if self.is_source_active(self._source):
            raise Exception(f"source ({self._source}) is inactive")
        # this store results of crawling
        crawl_output = None
        # try crawling for value in attempt
        for attempt in range(attempts):
            # check if source is active(e.g file available)
            if self.is_source_active(self._source):
                # star crawling
                crawl_output = self.crawl(self._source)
                self.crawled = True
                # update to show that crawl passed/successful
                if crawl_output != None:
                    self.status = 200
            # update to show that source was crawled
            self.crawled = True
            # dont retry if crawl succeeded
            if self.status == 200:
                break
            # sleep before retrying to crawl again
            time.sleep(attempt_inteval)
        if isinstance(crawl_output, str):
            # create sections from returned string
            self.sections = self.create_sections(crawl_output)
        elif isinstance(crawl_output, list):
            # initialise section objects from returned section objects
            self.sections = crawl_output
        elif crawl_output == None:
            # crawling failed to return data
            self.status = 1000
            self.failed = True
        else:
            # theres problem with output of crawl(self, source)
            raise Exception(f"crawl_output should be list, str or None not",
            type(crawl_output))
        return self.sections.copy()



if __name__ == "__main__":
    import os, sys

    crawl_obj = Crawl_Base("source of text", "title of resource")
    # read the current source file(this module)
    module_folder = os.path.dirname(__file__)
    text = open(os.path.join(module_folder, "crawl_base.py"), "r").read()
    # create section objects
    sections = crawl_obj.create_sections(text, 400)
    # add section objects
    crawl_obj.set_sections(sections)
    # print the last section object
    print(crawl_obj[-1])
