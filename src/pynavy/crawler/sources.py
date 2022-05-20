import os
from urllib.parse import urlparse
import mimetypes, re, glob

from .fetch import *
from .parse import *
from ..utility import directories

from bs4 import BeautifulSoup


def is_url(source: str):
    '''Checks if source is url\n
    source - resource locator e.g url, filepath'''
    return Web_Fetch.is_source_valid(source)

def is_local_file(source: str):
    '''Checks if source is a local file path\n
    source - resource locator e.g url, filepath'''
    return File_Fetch.is_file_path_valid(source)

def is_web_file(source: str):
    '''Checks if source is url pointing to file\n
    source - resource locator e.g url, filepath'''
    if is_url(source):
        # extract the path part of url
        url_path = urlparse(source).path
        # its  file if it has extension
        return bool(directories.get_file_extension(url_path))
    return False

def is_file(source: str):
    '''Checks if source point to a file(local or web)\n
    source - resource locator e.g url, filepath'''
    return is_local_file(source) or is_web_file(source)


def is_pdf_file(source: str):
    '''Checks if source is pdf file path\n
    source - resource locator e.g url, filepath'''
    return PDF_Parse.is_source_parsable(source)

def is_docx_file(source: str):
    '''Checks if source is pdf file path\n
    source - resource locator e.g url, filepath'''
    return DOCX_Parse.is_source_parsable(source)

def is_pptx_file(source: str):
    '''Checks if source is pptx file path\n
    source - resource locator e.g url, filepath'''
    return PPTX_Parse.is_source_parsable(source)

def is_html_file(source: str):
    '''Checks if source is html file path\n
    source - resource locator e.g url, filepath'''
    return HTML_Parse.is_source_parsable(source)

def is_text_file(source: str):
    '''Checks if source is text file path\n
    source - resource locator e.g url, filepath'''
    return Text_Parse.is_source_parsable(source)


def get_sources_from_text(text: str):
    '''Returns collection of urls and file paths\n
    text - text to extract sources(urls, file paths)'''
    pattern = r"(\b.*)(\/.*?\/)((?:[^\/]|\\\/)+?)(?:(?<!\\)\s|$)"
    urls = re.findall(pattern, text)
    sources = set()
    for rr in urls:
        sources.add("".join(rr))
    return sources

def get_urls_from_html(html: str):
    '''Extracts urls from html\n
    html - text with html'''
    sources = set()
    soup = BeautifulSoup(html, features="html")
    for link in soup.find_all("a"):
        sources.add(link.attrs['href'])
    return sources

def get_file_paths(folder_path: str, recursive=False):
    '''Returns file paths in from folder\n
    folder_path - path to folder with files\n
    recursive - true to search subdirectories'''
    return directories.get_file_paths(folder_path, recursive)


if __name__ == "__main__":
    # __name__ is not web file
    print(is_web_file(__name__))
