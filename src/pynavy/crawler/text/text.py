from .section import Section
from .metadata import Metadata

class Text(Metadata):
    '''Class for representing text broken into sections'''
    def __init__(self, source="unknown", title="unknown", 
        section_max_size=100000, metadata={}) -> None:
        '''
        source - can be file path, webpage url, etc(used to locate text)\n
        title - title of text\n
        section_max_size - maximum allowed section size\n
        metadata - dictionary to store extra data\n
        '''
        super().__init__(metadata)
        # can be file path, webpage url, etc
        self._source = source
        # main title for text
        # for webpage, <title>title</title>
        self._title = title
        # allowed maximum size of section
        self.section_max_size = section_max_size
        # stores section objects
        self.sections = []

        self.__sections_iter = iter(self.sections)

    def get_start_end_indexes(self, text_size, section_size):
        '''Generate start and end indexes from interger(section_size, text_size)\n
        End indexes are excluded just like Python lists(slicing)\n\n
        text_size - size of text in characters\n
        section_size - size of each section in characters
        '''
        assert isinstance(text_size, int)
        assert isinstance(section_size, int)
        assert section_size <= text_size, f"size({section_size}) should be less\
            than text_size({text_size})"
        # this will help when creating indexes
        quotient, remainder = divmod(text_size, section_size)
        # generate end indexes
        end_indexes = []
        for index in range(section_size-1, text_size, section_size):
            end_indexes.append(index+1)
        # use end indexes to create start_end_indexes
        # start_index = end_index-section_size+1
        start_end_indexes = list(map(lambda x: (x-section_size, x), end_indexes))
        # add the remaining start_end index if missing
        start_index, end_index = start_end_indexes[-1]
        if end_index != text_size:
            assert end_index < text_size, f"end_index{end_index} is out of\
            range 0-{text_size}"
            # add the remaining start end indexes
            start_end_indexes.append((end_index, text_size))
            assert end_indexes[-1] <= text_size, f'''end_index{start_end_indexes[-1][1]}
            is out of range'''
        # fix issue caused by range(section_size-1) at top
        # make start_index for first index 0 instead of 1
        #start_end_indexes[0] = (0, start_end_indexes[0][1])
        return start_end_indexes

    def create_section(self, text, start_end_index):
        '''Create section object from text and index. Section text get extracted from
        the text using start_end_index\n\n
        text - text to be sliced with start_end_index\n
        start_end_index - start and end index to extract section text\n'''
        assert(isinstance(text, str))
        assert(isinstance(start_end_index, tuple))
        start, end = start_end_index
        assert len(text) >= end or start>0, f"start_end_index({start_end_index})\
            out of range text{len(text)}"
        assert end > start, f"start_index({start})\
            is greater than end_index({end})"
        section_text = text[start:end]
        return Section(section_text, start_end_index)

    def create_sections(self, text, max_section_size=None) -> list:
        '''Create section objects from text\n\n
        text - text to create section objects from\n
        max_section_size - maximum size of each section(last section may not be)'''
        assert isinstance(text, str)
        assert isinstance(max_section_size, int) or max_section_size == None
        text_length = len(text)
        # calculate max_section_size if not provided
        if max_section_size == None:
            possible_section_size = 100000
            if text_length > possible_section_size:
                max_section_size = possible_section_size
            else:
                max_section_size = text_length
        assert len(text) >= max_section_size, "max_section_size is larger than text"
        start_end_indexes = self.get_start_end_indexes(text_length, max_section_size)
        sections = []
        for start_end_index in start_end_indexes:
            section_obj = self.create_section(text, start_end_index)
            sections.append(section_obj)
        return sections
    
    
    def size(self) -> int:
        '''Returns total sections'''
        return len(self.sections)

    def get_title(self) -> str:
        return self._title

    def get_source(self) -> str:
        return self._source

    def set_sections(self, sections) -> None:
        '''Overide section objects with list of section objects'''
        assert isinstance(sections, list)
        self.sections = sections

    def get_sections(self) -> list:
        '''Returns list of section objects'''
        return self.sections

    def add_section(self, section_obj) -> None:
        '''Add section object
        section_obj - section object to add'''
        assert section_obj.__class__ == Section, Section
        assert self.section_max_size >= section_obj.size(), f"section is too large, \
        with size {section_obj.size()} instead of {self.section_max_size}"
        self.sections.append(section_obj)

    def filter_sections(self, function) -> list:
        '''Filter section objects based on function'''
        assert callable(function), type(function) + "is not callable"
        return list(filter(function, self.sections))

    def get_sections(self, function=None) -> list:
        '''Filter section objects based on function'''
        if function == None:
            return self.sections
        assert callable(function), type(function) + "is not callable"
        raise self.filter_sections(self.sections, function)
    
    def remove_section(self, function) -> None:
        assert callable(function), type(function) + "is not callable"
        for section in self.sections:
            if function(section):
                return self.sections.remove(section)
        raise ValueError("Section object not found")

    def section_exists(self, function) -> bool:
        '''Checks existance of section based on function'''
        assert callable(function), type(function) + "is not callable"
        for section in self.sections:
            if function(section):
                return True
        return False
    
    def clear(self) -> None:
        '''Clears all sections and metadata'''
        self.sections.clear()
        self.clear_metadata()

    def get_text(self) -> str:
        '''Returns text of Text obj'''
        text = ""
        for section in self.sections:
            text += section.get_text()
        return text 

    # def __key(self):
    #     # key get computed from hashes of section objects
    #     # time complexity is expected to be linear
    #     # this will impact speed of == and != also hash()
    #     # changes to section objects would change return value
    #     # which could lead to poor performance in dict and sets
    #     return (*self.sections,)

    def __key(self) -> int:
        if self._source != self._title:
            return hash((Text, self._source, self._title))
        return super().__hash__()
        

    def __iter__(self):
        self.__sections_iter = iter(self.sections)
        return self.__sections_iter

    def __next__(self):
        return next(self.__sections_iter)

    def __len__(self, /) -> int:
        return self.size()

    def __eq__(self, other, /):
        if isinstance(other, Text):
            return self.__key() == other.__key()
        return NotImplemented
    
    def __ne__(self, other, /):
        if isinstance(other, Text):
            return self.__key() != other.__key()
        raise NotImplemented

    def __bool__(self, /):
        return self.size() > 0
    
    def __getitem__(self, key) -> Section:
        return self.sections[key]

    def __contains__(self, key, /) -> bool:
        return key in self.sections

    def __hash__(self) -> int:
        return self.__key()

if __name__ == "__main__":
    text_obj = Text("", "")
    text = "abcdefghij"
    indexes = text_obj.get_start_end_indexes(len(text), 2)
    for index in indexes:
        print(index[0], index[1])
    print("finished", len(text), len(indexes))



