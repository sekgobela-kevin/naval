from ...utility.section import Section
from ...utility.equality import Equality
class Text_Section(Section, Equality):
    '''Represents portion of text'''
    def __init__(self, text, start_end_index, metadata={}) -> None:
        super().__init__(text, start_end_index, metadata)
    
    def get_text(self) -> str:
        '''Returns text of section'''
        return self.get_elements()

    
    def __add__(self, value, /):
        # combine text of sections
        text = self.text + value.text
        # combine indexes by taking smallest and largest index
        combined_indexes = self.start_end_index + value.start_end_index
        start_end_indexes = (min(combined_indexes), max(combined_indexes))
        return Text_Section(text, start_end_indexes)

    def _key(self) -> int:
        return hash(self.get_text())
