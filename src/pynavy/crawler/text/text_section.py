from ...utility.section import Section

class Text_Section(Section):
    '''Represents portion of text'''
    def __init__(self, text, start_end_index, metadata={}) -> None:
        super().__init__(text, metadata)
        # contains start and end(included) index of text
        self.start_end_index = start_end_index
        self.start_index = start_end_index[0]
        self.end_index = start_end_index[1]

    def get_index(self):
        return self.start_end_index
    
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

    def __hash__(self) -> int:
        return hash(self.get_text())

    def __eq__(self, other) -> bool:
        return self.__hash__() == hash(other)
