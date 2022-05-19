from urllib.parse import urlparse

from .fetch import *
from .parse import *

from ..utility import directories

import mimetypes

def is_url(source):
    '''Checks if source is url'''
    return Web_Fetch.is_source_valid(source)

def is_local_file(source):
    '''Checks if source is a local file path'''
    return File_Fetch.is_file_path_valid(source)

def is_web_file(source):
    '''Checks if source is url pointing to file'''
    if is_url(source):
        # extract the path part of url
        url_path = urlparse(source).path
        # its  file if it has extension
        return bool(directories.get_file_extension(url_path))
    return False

def is_file(source):
    '''Checks if source point to a file(local or web)'''
    return is_local_file(source) or is_web_file(source)


def is_pdf_file(source):
    '''Checks if source is pdf file path'''
    return PDF_Parse.is_source_parsable(source)

def is_docx_file(source):
    '''Checks if source is pdf file path'''
    return DOCX_Parse.is_source_parsable(source)

def is_pptx_file(source):
    '''Checks if source is pptx file path'''
    return PPTX_Parse.is_source_parsable(source)

def is_html_file(source):
    '''Checks if source is html file path'''
    return HTML_Parse.is_source_parsable(source)

def is_text_file(source):
    '''Checks if source is text file path'''
    return Text_Parse.is_source_parsable(source)


if __name__ == "__main__":
    # __name__ is not web file
    print(is_web_file(__name__))