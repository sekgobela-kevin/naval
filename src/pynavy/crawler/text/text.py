from ...utility.container import Container
from .text_section import Text_Section

class Text(Container):
    '''Class for representing text broken into sections'''
    def __init__(self, source, title, text="", 
        section_max_size=100000, metadata={}) -> None:
        '''
        source - can be file path, webpage url, etc(used to locate text)\n
        title - title of text\n
        section_max_size - maximum allowed section size\n
        metadata - dictionary to store extra data\n
        '''
        # can be file path, webpage url, etc
        self._source = source
        # main title for text
        # for webpage, <title>title</title>
        self._title = title
        # allowed maximum size of section
        self.section_max_size = section_max_size
        # create sections from string text
        sections = self.create_sections(text, section_max_size)
        super().__init__(sections, metadata)

    def create_start_indexes(self, text_size, section_size) -> list:
        '''Create end indexes\n
        text_size - size of text in characters\n
        section_size - size of each section in characters'''
        start_indexes = []
        for index in range(0, text_size, section_size):
            start_indexes.append(index) 
        return tuple(start_indexes)

    def create_end_indexes(self, text_size, section_size) -> list:
        '''Create start indexes\n
        text_size - size of text in characters\n
        section_size - size of each section in characters
        '''
        end_indexes = []
        for index in range(section_size, text_size, section_size):
            end_indexes.append(index) 
        # add last index if missing
        # only if last text_size is not zero
        if text_size>0 and (text_size not in end_indexes):
            end_indexes.append(text_size)
        return tuple(end_indexes)

    def create_start_end_indexes(self, text_size, section_size):
        '''Creates start and end indexes
        text_size - size of text in characters\n
        section_size - size of each section in characters
        '''
        assert isinstance(text_size, int), type(text_size)
        assert isinstance(section_size, int), type(section_size)
        start_indexes = self.create_start_indexes(text_size, section_size)
        end_indexes = self.create_end_indexes(text_size, section_size)
        start_end_indexes = map(lambda x,y: (x,y), start_indexes, end_indexes)
        return tuple(start_end_indexes)

    def create_section(self, text, start_end_index):
        '''Create section object from text and index. Section text get extracted from
        the text using start_end_index\n\n
        text - text to be sliced with start_end_index\n
        start_end_index - start and end index to extract section text\n'''
        assert(isinstance(text, str))
        assert(isinstance(start_end_index, tuple))
        start, end = start_end_index
        if start > end:
            raise Exception(f"start_index({start}) is greater than \
            end_index({end}")
        # check if start_end_index is out of range
        if start < 0 or end > len(text):
            raise Exception(f"start_end_index({start_end_index} out range\
            to text of length {len(text)}")
        section_text = text[start:end]
        return Text_Section(section_text, start_end_index)

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
        # create start_end_indexes for text sections
        start_end_indexes = self.create_start_end_indexes(text_length, 
            max_section_size)
        sections = []
        for start_end_index in start_end_indexes:
            section_obj = self.create_section(text, start_end_index)
            sections.append(section_obj)
        return sections

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

    def get_text(self) -> str:
        '''Return text from all section objects'''
        text = ""
        for section in self.sections:
            text += section.get_text()
        return text 

    def __hash__(self) -> int:
        # text with same source and title are equal
        return hash(self._source)

    def __eq__(self, other) -> bool:
        return self.__hash__() == hash(other)

if __name__ == "__main__":
    text_obj = Text("", "", "abcdefghij"*40000, 100)
    
    print(text_obj != "")



