from io import FileIO, IOBase
import os
import shutil
from typing import List

from .parse.parse_base import Parse_Base
from .crawl import Crawl

from .fetch import *
from .parse import *
from .text import *

from ..utility.container import Container
from . import sources
from ..utility import directories


def create_start_end_indexes(collection_size: int, split_size: int):
    '''
    Returns start end indexes for sections of collection
    size - size of collection to be split(e.g list, str, set)\n
    split_size - range of each index
    '''
    return Container.create_start_end_indexes(collection_size, split_size)

def split_text(text: str, split_size: int) -> List[str]:
    '''Split text into smaller sections\n
    text - text to be split to smaller sections\n
    split_size - size of each section'''
    text_sections: List[str] = []
    # get start and end indexes for each section
    start_end = create_start_end_indexes(len(text), split_size)
    for start, end in start_end:
        text_sections.append(text[start:end])
    return text_sections

def create_text_sections(text: str, split_size: int) -> List[Text_Section]:
    '''Split text into text section objects\n
    text - text to be split to smaller sections\n
    split_size - size of each section'''   
    text_sections: List[Text_Section] = []
    for start, end in create_start_end_indexes(len(text), split_size):
        start_end = (start, end)
        section_text = text[start:end]
        text_sections.append(Text_Section(section_text, start_end))
    return text_sections

def sections_to_text(sections_obj: List[Text_Section]) -> List[str]:
    '''Returns list with text of each section object\n
    sections_objs - list of text section objects'''
    return [section.get_text() for section in sections_obj]

def get_start_end_indexes(sections_texts: List[str]):
    '''Returns start, end indexes from list of texts\n
    sections_texts - list of texts for each section'''
    start_end_indexes = []
    # calculate star and end indexes from sections_texts
    # start_index and end_index will be changed in loop
    start_index = 0
    end_index = 0
    for sections_text in sections_texts:
        # increment end index
        # start index does not need to be incremented
        end_index += len(sections_text)
        start_end_indexes.append((start_index, end_index))
        # increment start index to be used next
        start_index += len(sections_text)
    return tuple(start_end_indexes)


def get_file_object(file, **kwarg):
    '''Return file object from file path or anothe file object\n
    file - string file path or file like object\n
    kwarg - optional keywords arguments to pass to open()'''
    if isinstance(file, str):
        file_obj = open(file, **kwarg)
    elif isinstance(file, IOBase):
        file_obj = file
    else:
        err_msg = "file should be str file path or file object"
        raise TypeError(err_msg, type(file))
    return file_obj

def copy_file(src_file, dest_file):
    '''Copy file in from src_file to dest_file\n
    src_file - source string file path or file like object\n
    src_file - destination string file path or file like object'''
    # create file objects
    src_file_obj = get_file_object(src_file)
    dest_file_obj = get_file_object(dest_file)
    # seek to begining of files
    dest_file.seek(0)
    src_file_obj.seek(0)
    # write source file into destination
    dest_file.writelines(src_file)
    # close files
    src_file.close()
    dest_file.close()



def download(url: str, file: str or IOBase) -> None:
    '''Download data from url into file\n
    url -url to webpage or web file\n
    file - string file path or file like object'''
    # create fetch object and request for data
    fetch_obj = Web_Fetch(url)
    # this writes to file kept by fetch object
    fetch_file = fetch_obj.request()
    copy_file(fetch_file, file)
    # its expected to be slow due to multiple writing
    # one in fetch object and one in this function
    # it takes 2 opened files to complete the function

def download_all(folder_path: str, urls: List[str]) -> None:
    '''Download data from urls into folder\n
    folder_path - Folder to download into\n
    urls - list of urls'''
    if not os.path.isdir(folder_path):
        raise Exception(f"folder_path{folder_path} is not folder")
    for url in urls:
        # create filename from url
        filename = Web_Fetch.get_filename_from_url(url)
        # add .html to filename if not path part to url
        # its likely to be webpage which is mostly HTML
        if not sources.get_url_path(url):
            filename += ".html"
        filepath = os.path.join(folder_path, filename)
        # download data in url and store to filepath
        download(url, filepath)


def get_fetch_object(source) -> Fetch_Base:
    '''Returns fetch with data for source\n
    source - url, file path or gile object, etc'''
    # returns that fetch object if fetch is fetch object
    # list() also returns list if passed list
    if isinstance(source, Fetch_Base):
        return source
    if not Master_Fetch.fetch_class_exists(source):
        err_msg = f"source({source}) is not fetchable(no fetch class)"
        raise Exception(err_msg)
    fetch_obj = Master_Fetch.get_fetch_object(source)
    fetch_obj.request()
    # Fetch(source) could also work
    return fetch_obj

def get_parse_object(fetch_input) -> Parse_Base:
    '''Returns parse object for fetch object or fetch source\n
    fetch_input - source(url, file path, etc) or fetch object'''
    # returns the parse object if fetch_input is parse object
    # users wont notice anything
    # list() returns list if passed list
    if isinstance(fetch_input, Parse_Base):
        return fetch_input
    else:
        # fetch_input is source or fetch object
        fetch_obj = get_fetch_object(fetch_input)
    if not Master_Parse.is_fetch_valid(fetch_obj):
        # parse class wasnt registed or problem with source extension
        source = fetch_obj.get_source
        err_msg = f"source({source}) is not parsable(no parse class)"
        raise Exception(err_msg)
    # Parse(fetch_obj) could also work
    return Master_Parse.get_parse_object(fetch_obj)

def get_crawl_object(source):
    '''Creates and returns crawl object\n 
    source - url, file path or gile object, etc'''
    return Crawl(source)


def extract_text(parse_input) -> str:
    '''Extract text from source, fetch object or parse object\n
    parse_input - source(url, file path, etc), fetch object or parse object'''
    return get_parse_object(parse_input).get_text()

def extract_html(parse_input) -> str:
    '''Extract html from source, fetch object or parse object\n
    parse_input - source(url, file path, etc), fetch object or parse object'''
    return get_parse_object(parse_input).get_html()

def extract_text_to_file(parse_input, dest_file) -> str:
    '''Extract text from source, fetch object or parse object\n
    parse_input - source(url, file path, etc), fetch object or parse object\n
    dest_file - destination string file path or file like object'''
    # this is a temporary solution
    # get_parse_object() returns parse object with file closed
    # __del__ was called as end of function was reached
    # solution is to use context managers(with statement)
    dest_file_obj = get_file_object(dest_file, mode="w")
    dest_file_obj.write(extract_text(parse_input))
    dest_file_obj.close()

def extract_html_to_file(parse_input, dest_file) -> str:
    '''Extract text from source, fetch object or parse object\n
    parse_input - source(url, file path, etc), fetch object or parse object\n
    dest_file - destination string file path or file like object'''
    dest_file_obj = get_file_object(dest_file, mode="w")
    dest_file_obj.write(extract_html(parse_input))
    dest_file_obj.close()


if __name__ == "__main__":
    print(get_start_end_indexes(create_text_sections("namename", 4)))
