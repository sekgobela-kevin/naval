from io import IOBase, StringIO
import tempfile

import pptx

from .parse_base import Parse_Base

class Text_Parse(Parse_Base):
    '''Parses text from fetch object'''
    # fetch object with text is expected
    # use "text/" for all text files
    # and "text/plain" for plain text eg .txt
    fetch_content_type = "text/"
    # given low priority
    # html files should use html parse not text parse
    priority = 5

    def __init__(self, fetch_obj) -> None:
        super().__init__(fetch_obj)

    def text_to_file(self):
        '''Parses text and store it to self.text_file'''
        fetch_file = self.fetch_obj.get_file()
        fetch_file.seek(0)
        self.text_file.truncate(0)
        for line in fetch_file:
            # handle exception if files opended in different modes
            # writing bytes to text file would raise errors
            try:
                self.text_file.write(line)
            except TypeError:
                self.text_file.write(line.decode())
        return self.text_file

if __name__ == "__main__":
    from ..fetch.master_fetch import Master_Fetch
    from ..fetch.web_fetch import Web_Fetch

    # create fetch object
    fetch_obj = Master_Fetch.get_fetch_object(open(__file__))
    # this performs request for data
    fetch_obj.request()
    print(len(fetch_obj.fetch()))

    # create parse object from fetch object
    parse_obj = Text_Parse(fetch_obj)
    print(parse_obj.get_text())