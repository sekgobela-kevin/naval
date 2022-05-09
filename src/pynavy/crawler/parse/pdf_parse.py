import logging
import sys
from io import BytesIO, IOBase, StringIO
from typing import Any, BinaryIO, Container, Iterator, Optional, cast

from pdfminer.converter import (XMLConverter, 
    PDFConverter, HTMLConverter, TextConverter, 
    PDFPageAggregator
)
from pdfminer.image import ImageWriter
from pdfminer.layout import LAParams, LTPage
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.utils import open_filename, FileOrName, AnyIO

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

# the high level api
from pdfminer.high_level import extract_text_to_fp
from pdfminer.high_level import extract_text

from .parse_base import Parse_Base


class PDF_Parse(Parse_Base):
    '''Parses pdf data from fetch object'''
    def __init__(self, fetch_obj) -> None:
        super().__init__(fetch_obj)
        # specify type of doc object(type annotation)
        print("creating doc")
        self.doc = self.create_doc()
        print("creating res manc")
        self.pdf_res_man = PDFResourceManager()

    def create_doc(self) -> PDFDocument:
        '''Create PDFDocument object(the object is not used)'''
        parser = PDFParser(fetch_obj.get_file())
        return PDFDocument(parser)

    def get_title(self) -> None:
        '''Returns title tag text'''
        return None

    @staticmethod
    def _pdf_convert(output_string:IOBase, pdf_doc:PDFDocument, 
            pdf_res_man:PDFResourceManager, 
            pdf_converter_class:PDFConverter):
        '''Convert pdf to format specified by device. The function is
        meant for reusing functionality of low level api of pdfminer'''
        # clear everything in file object
        output_string.truncate(0)
        # creates of converter object(convert pdf to another format)
        device = pdf_converter_class(pdf_res_man, output_string, 
        codec="utf-8", laparams=LAParams(), imagewriter=None)
        # Processor for the content of a PDF page(from its docstring)
        interpreter = PDFPageInterpreter(pdf_res_man, device)
        for page in PDFPage.create_pages(pdf_doc):
            # instruct interpreter to proccess the page
            interpreter.process_page(page)


    def get_text(self) -> str or bytes:
        print("getting text")
        '''Retuns text version of fetch object'''
        # string stream to store extracted html
        output_string = BytesIO()
        PDF_Parse._pdf_convert(output_string, self.doc, self.pdf_res_man, 
        TextConverter)
        return output_string.getvalue()

    def get_html(self) -> str:
        '''Retuns html version of fetch object'''
        # string stream to store extracted html
        output_string = BytesIO()
        PDF_Parse._pdf_convert(output_string, self.doc, self.pdf_res_man,
        HTMLConverter)
        return output_string.getvalue()

    def text_to_file(self):
        '''Parses text and store it to file'''
        PDF_Parse._pdf_convert(self.file, self.doc, 
        self.pdf_res_man, TextConverter)
        return self.file

    def html_to_file(self):
        '''Parses html and store it to file'''
        PDF_Parse._pdf_convert(self.file, self.doc, 
        self.pdf_res_man, HTMLConverter)
        return self.file

if __name__ == "__main__":
    from ..fetch.web_fetch import Web_Fetch

    # create fetch object
    url = "https://gifs.africa/wp-content/uploads/2020/05/Grade-12-Mathematical-Literacy-Revision-Study-Guide.pdf"
    fetch_obj = Web_Fetch(url)
    # this performs request for data
    fetch_obj.request()

    # create parse object from fetch object
    parse_obj = PDF_Parse(fetch_obj)
    print(parse_obj.get_text())
