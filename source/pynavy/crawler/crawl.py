from .crawl_base import Crawl_Base

class Crawl(Crawl_Base):
    '''Main class for crawling data from source'''
    def __init__(self, source, section_max_size=100000, **kwarg):
        super().__init__(source, section_max_size, **kwarg)

if __name__ == "__main__":
    crawl_obj = Crawl("https://www.example.com")
    print(len(crawl_obj))