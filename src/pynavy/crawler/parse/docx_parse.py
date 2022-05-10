from io import StringIO
import zipfile

import docx
from docx.parts.document import DocumentPart

from pydocx import PyDocX
from pydocx.export import PyDocXHTMLExporter
from pydocx.exceptions import MalformedDocxException

from .parse_base import Parse_Base
from .html_parse import HTML_Parse
from ..fetch.file_fetch import File_Fetch

class DOCX_Parse(Parse_Base):
    '''Parses html data from fetch object'''
    def __init__(self, fetch_obj) -> None:
        super().__init__(fetch_obj)
        self.doc: docx.document.Document

    def create_doc(self, *args, **kwarg) -> docx.document.Document:
        '''Return object to use when parsing fetch object contents.'''
        return docx.Document(self.fetch_obj.get_file())

    def text_to_file(self):
        '''Parses text and store it to self.text_file'''
        for paragraph in self.doc.paragraphs:
            for run in paragraph.runs:
                self.text_file.write(run.text+"\n")
        return self.text_file

    def html_to_file(self):
        '''Parses html and store it to self.html_file'''
        html = PyDocX.to_html(self.fetch_obj.get_file())
        self.html_file.write(html)
        return self.html_file

if __name__ == "__main__":
    from ..fetch.file_fetch import File_Fetch

    # create fetch object
    file_path = "path to file.docx"
    fetch_obj = File_Fetch(file_path)
    # this performs request for data
    fetch_obj.request()

    # create parse object from fetch object
    parse_obj = DOCX_Parse(fetch_obj)
    print(len(parse_obj.get_text()))
    print(len(parse_obj.get_text()))
    print(len(parse_obj.get_text()))
    print(len(parse_obj.get_html()))
