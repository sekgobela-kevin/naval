from io import FileIO, IOBase
import os
import shutil
from typing import List

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



def download(url: str, file: str or IOBase) -> None:
    '''Download data from url into file\n
    url -url to webpage or web file\n
    file - string file path or file like object'''
    if isinstance(file, str):
        file_obj = open(file, mode="w+b")
    elif isinstance(file, IOBase):
        file_obj = file
    else:
        err_msg = "file should be string or file object"
        raise TypeError(err_msg, type(file))
    # create fetch object and request for data
    fetch_obj = Web_Fetch(url)
    # this writes to file kept by fetch object
    fetch_file = fetch_obj.request()
    fetch_file.seek(0)
    # copy fetch object file contents to requested file
    file_obj.writelines(fetch_file)
    file_obj.close()
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


        
    

if __name__ == "__main__":
    print(get_start_end_indexes(create_text_sections("namename", 4)))