from io import IOBase
from typing import Type

from ..fetch.fetch_base import Fetch_Base
from .parse_base import Parse_Base
from .master_parse import Master_Parse


class Parse(Parse_Base, Master_Parse):
    '''Main class for parsing data from fetch object'''
    def __init__(self, fetch_obj: Fetch_Base) -> None:
        # get parse object from fetch object
        self.parse_obj = Master_Parse.get_parse_object(fetch_obj)
        # set type annotation for doc to match that of parse object
        self.doc : Type[self.parse_obj.doc] = self.parse_obj.get_doc()
        super().__init__(fetch_obj)

    def create_doc(self):
        '''Create document for pasing data(depends on library used)'''
        return self.parse_obj.doc

    def text_to_file(self) -> IOBase:
        '''Extract text and store it to file'''
        # extract text from fetch object
        self.parse_obj.text_to_file()
        # share text data of parse obj with self.text_file
        self.parse_obj.get_text_file().seek(0)
        for line in self.parse_obj.get_text_file():
            self.text_file.write(line)
        return self.text_file

    def html_to_file(self) -> IOBase:
        '''Extract HTML and store it to file'''
        # extract HTML from fetch object
        self.parse_obj.html_to_file()
        # share html data of parse obj with self.html_file
        self.parse_obj.get_html_file().seek(0)
        for line in self.parse_obj.get_html_file():
            self.html_file.write(line)
        return self.html_file

    def get_parse(self):
        '''Returns parse underlying parse object'''
        return self.parse_obj

if __name__ == "__main__":
    from ..fetch.fetch import Fetch

    fetch_obj = Fetch("https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_core_sql_expressions.htm")
    fetch_obj.request()

    parse_obj = Parse(fetch_obj)
    parse_obj.get_doc()
    print(parse_obj.get_html())
