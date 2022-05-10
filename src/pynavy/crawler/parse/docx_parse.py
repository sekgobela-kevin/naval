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

    def _get_text_pydocx(self) -> str or bytes:
        '''Retuns text using pydocx library'''
        # text get retrieved from HTML
        # string to store html to pass to fetch object
        string_io = StringIO(self.get_html())
        # create fetch object to pass to html parse object
        parse_obj = File_Fetch(string_io)
        # create html parse objetc
        parse_obj = HTML_Parse(parse_obj)
        # extract text from it
        return parse_obj.get_text()

    def _get_text_python_docx(self):
        '''Retuns text using python-docx library'''
        text_list = []
        for paragraph in self.doc.paragraphs:
            for run in paragraph.runs:
                text_list.append(run.text)
        return "\n".join(text_list)

    def _get_text_pydocx(self) -> str or bytes:
        '''Retuns text using pydocx library'''
        # text get retrieved from HTML
        # string to store html to pass to fetch object
        string_io = StringIO(self.get_html())
        # create fetch object to pass to html parse object
        parse_obj = File_Fetch(string_io)
        # create html parse objetc
        parse_obj = HTML_Parse(parse_obj)
        # extract text from it
        return parse_obj.get_text()

    def get_text(self):
        '''Retuns text version of fetch object'''
        try:
            return self._get_text_python_docx()
        except zipfile.BadZipFile:
            return self._get_text_pydocx()
        

    def get_html(self) -> str:
        '''Retuns html version of fetch object'''
        return PyDocX.to_html(self.fetch_obj.get_file())

if __name__ == "__main__":
    from ..fetch.file_fetch import File_Fetch

    # create fetch object
    url = "/mnt/c/university/1st year/1st semester/Term 1/Reflection on teaching and learning/blackboard notes/4_3_4 Accelerator Model.docx"
    fetch_obj = File_Fetch(url)
    # this performs request for data
    fetch_obj.request()

    # create parse object from fetch object
    parse_obj = DOCX_Parse(fetch_obj)
    print(parse_obj.get_text())