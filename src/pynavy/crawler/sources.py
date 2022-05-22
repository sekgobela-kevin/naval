import os
from urllib.parse import urlparse
import mimetypes, re, glob

from src.pynavy.utility import directories
from bs4 import BeautifulSoup

if mimetypes.inited: 
    mimetypes.init()

def is_url(source: str):
    '''Checks if source is url\n
    source - resource locator e.g url, filepath'''
    try:
        parsed = urlparse(source )
        return all([parsed.scheme, parsed.netloc])
    except:
        return False

def get_url_path(url: str) -> None or str:
    '''Extracts path part from url\n
    url - url of webpage or web file'''
    return urlparse(url).path

def is_local_file(source: str):
    '''Checks if source is a local file path\n
    source - resource locator e.g url, filepath'''
    pattern = r"(\b.*)(\/.*?\/)((?:[^\/]|\\\/)+?)(?:(?<!\\)\s|$)"
    if not is_url(source):
        return bool(re.search(pattern, source))
    return False

    

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
    source_type = mimetypes.guess_type(source)[0]
    ext_type = mimetypes.guess_type(" .pdf")[0]
    return source_type == ext_type

def is_docx_file(source: str):
    '''Checks if source is pdf file path\n
    source - resource locator e.g url, filepath'''
    source_type = mimetypes.guess_type(source)[0]
    ext_type = mimetypes.guess_type(" .docx")[0]
    return source_type == ext_type

def is_pptx_file(source: str):
    '''Checks if source is pptx file path\n
    source - resource locator e.g url, filepath'''
    source_type = mimetypes.guess_type(source)[0]
    ext_type = mimetypes.guess_type(" .pptx")[0]
    return source_type == ext_type

def is_html_file(source: str):
    '''Checks if source is html file path\n
    source - resource locator e.g url, filepath'''
    source_type = mimetypes.guess_type(source)[0]
    ext_type = mimetypes.guess_type(" .html")[0]
    return source_type == ext_type

def is_plain_text_file(source: str):
    '''Checks if source is text file path\n
    source - resource locator e.g url, filepath'''
    source_type = mimetypes.guess_type(source)[0]
    ext_type = mimetypes.guess_type(" .txt")[0]
    return  ext_type == source_type

def is_txt_file(source: str):
    '''Checks if source is text file path\n
    source - resource locator e.g url, filepath'''
    return is_plain_text_file(source)

def is_text_file(source: str):
    '''Checks if source is text file path\n
    source - resource locator e.g url, filepath'''
    source_type = mimetypes.guess_type(source)[0]
    return  "text/" in source_type




def get_urls_from_text(text: str, sep:str="\n", strict=False):
    '''Extracts urls from text\n
    text - text to extract sources(urls, file paths)'''
    pattern = r"(https:\/\/)(.*?\/)((?:[^\/]|\\\/)+?)(?:(?<!\\)\s|$)"
    urls = set()
    for url in re.findall(pattern, text):
        if url:
            urls.add("".join(url).strip())
    return urls
    
def get_urls_from_html(html: str):
    '''Extracts urls from html\n
    html - text with html'''
    sources = set()
    soup = BeautifulSoup(html, features="lxml")
    for link in soup.find_all("a"):
        sources.add(link.attrs['href'])
    return sources

def get_file_paths(folder_path: str, recursive=False):
    '''Returns file paths in from folder\n
    folder_path - path to folder with files\n
    recursive - true to search subdirectories'''
    return set(directories.get_file_paths(folder_path, recursive))


if __name__ == "__main__":
    # __name__ is not web file
    print(is_web_file(__name__))
