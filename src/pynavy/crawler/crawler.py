from typing import List
from .fetch import *
from .parse import *
from .text import *

from ..utility.container import Container
from . import sources

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


if __name__ == "__main__":
    print(get_start_end_indexes(create_text_sections("namename", 4)))
