from io import StringIO

import pptx

from .parse_base import Parse_Base

class Text_Parse(Parse_Base):
    '''Parses text from fetch object'''
    def __init__(self, fetch_obj) -> None:
        super().__init__(fetch_obj)
        self.text_file = self.fetch_obj.get_file()

    def text_to_file(self):
        '''Parses text and store it to self.text_file'''
        fetch_file = self.fetch_obj.get_file()
        fetch_file.seek(0)
        self.text_file.truncate(0)
        for line in fetch_file:
            self.text_file.write(line)
        return self.text_file

if __name__ == "__main__":
    from ..fetch.master_fetch import Master_Fetch
    from ..fetch.web_fetch import Web_Fetch

    # create fetch object
    fetch_obj = Master_Fetch.get_fetch_object(open(__file__, "r"))
    # this performs request for data
    fetch_obj.request()
    print(len(fetch_obj.fetch()))

    # create parse object from fetch object
    parse_obj = Text_Parse(fetch_obj)
    print(parse_obj.get_text())