import sys

from .metadata import Metadata

class Section(Metadata):
    '''Represents portion of text'''
    def __init__(self, text, start_end_index, metadata={}) -> None:
        super().__init__(metadata)
        # text of portion from text
        self.text = text
        # contains start and end(included) index of text
        self.start_end_index = start_end_index
        self.start_index = start_end_index[0]
        self.end_index = start_end_index[1]

        # to be used with __next__() and __iter__()
        self.__text_iter = iter(self.text)
    
    def get_text(self) -> str:
        '''Returns text of section'''
        return self.text
    
    def size(self) -> int:
        '''Returns size of text stored in the section'''
        return len(self.text)
    
    def __add__(self, value, /):
        text = self.text + value.text
        combined_indexes = self.start_end_index + value.start_end_index
        start_end_indexes = [min(combined_indexes), max(combined_indexes)]
        return Section(text, start_end_indexes)

    def __key(self):
        return (self.text, self.start_index, self.end_index)

    def __iter__(self):
        self.__text_iter = iter(self.text)
        return self.__text_iter

    def __next__(self):
        return next(self.__text_iter)

    def __len__(self, /):
        return self.size()

    def __eq__(self, other, /):
        if isinstance(other, Section):
            return self.__key() == other.__key()
        return NotImplemented
    
    def __ne__(self, other, /):
        if isinstance(other, Section):
            return self.__key() != other.__key()
        return NotImplemented

    def __bool__(self, /):
        return self.size() > 0
    
    def __getitem__(self, key):
        return self.text[key]

    def __contains__(self, key, /):
        return key in self.text

    def __hash__(self):
        return hash(self.__key())

