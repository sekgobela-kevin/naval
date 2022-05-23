from .metadata import Metadata

class Section(Metadata):
    '''Represents a portion e.g section of text.
    Use section object if theres need to break a large part into smaller
    parts. Section object represent a part and that part needs to be 
    iterable just like the larger part. \n
    
    Section object should not large. If its text, it should only cover smaller
    portion.'''
    def __init__(self, elements=[], start_end_index=(0,0), metadata={}) -> None:
        '''elements [iterable] - items which are part of section.\n
        metadata [dict] - extra data to store on object
        '''
        self.elements = elements
        self.start_end_index = start_end_index
        self.start_index = start_end_index[0]
        self.end_index = start_end_index[1]
        assert self.start_index <= self.start_index, start_end_index
        super().__init__(metadata)
        # to be used with __next__() and __iter__()
        # error will be raised if self.elements is not iterable
        self.__elements_iter = iter(self.elements)

    def get_index(self):
        return self.start_end_index

    def get_elements(self) -> str:
        '''Returns elemets of section'''
        return self.elements
    
    def size(self) -> int:
        '''Returns size of text stored in the section'''
        return len(self.elements)
    
    def __add__(self, value, /):
        # add elements of sections together
        # self metadata is passed to as metadata to result section
        elements = self.get_elements() + value.get_elements()
        return Section(elements, self.get_metadata())

    def __key(self):
        return (self.elements)

    def __iter__(self):
        self.__elements_iter = iter(self.elements)
        return self.__elements_iter

    def __next__(self):
        return next(self.__elements_iter)

    def __len__(self, /):
        return self.size()

    def __bool__(self, /):
        return self.size() > 0
    
    def __getitem__(self, key):
        return self.elements[key]

    def __contains__(self, key, /):
        return key in self.elements


if __name__ == "__main__":
    section_obj = Section("items")
    section_obj2 = Section()

    print("is equal", section_obj == section_obj2)
    for item in section_obj:
        print(item)
