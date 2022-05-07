from ...utility.container import Container
from ...utility.equality import Equality
from .text_section import Text_Section


class Text(Container, Equality):

    def __init__(self, source, title="", text="", 
        section_max_size=100000, metadata={}) -> None:
        '''
        source - used to to identify the text\n
        title - title of text\n
        text - initial text to use to create sections\n
        section_max_size - maximum allowed section size\n
        metadata - dictionary to store extra data\n
        '''
        if not isinstance(source, str):
            raise TypeError(f"source should be string not ", type(source))
        if not isinstance(title, str):
            raise TypeError(f"title should be string not ", type(title))
        if not isinstance(text, str):
            raise TypeError(f"text should be string not ", type(text))
        if not isinstance(metadata, dict):
            raise TypeError(f"text should be dict not ", type(metadata))

        super().__init__(metadata=metadata)
        # can be file path, webpage url, etc
        self._source = source
        # main title for text
        # for webpage, <title>title</title>
        self._title = title
        # allowed maximum size of section
        self.section_max_size = section_max_size
        # tell Container to use Text_Section instead of Section class
        self._section_class = Text_Section

    def get_title(self) -> str:
        return self._title

    def get_source(self) -> str:
        return self._source

    def get_text(self) -> str:
        '''Return text from all section objects'''
        text = ""
        for section in self.sections:
            text += section.get_text()
        return text 

    def _key(self) -> int:
        # text with same source and title are equal
        return hash(self._source)

if __name__ == "__main__":
    text_obj = Text("", "", "abcdefghij"*40000, 100)
    
    print(text_obj != "")



