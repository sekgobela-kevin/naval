from .section import Section
from .metadata import Metadata
from .equality import Equality

class Container(Metadata):
    '''Class for representing collection of section object'''
    def __init__(self, sections=[], metadata={}) -> None:
        '''
        sections [collection] - collection of section objects
        '''
        if not self.contains_sections(sections):
            raise TypeError("sections contain non Section objects")
        super().__init__(metadata)
        # stores section objects
        self.sections = list(sections)
        # iterator to section objects
        self.__sections_iter = iter(self.sections)
    
    def contains_sections(self, sections):
        '''Checks if items in collection are section objects'''
        return all([isinstance(section, Section) for section in sections])

    def create_section(self, *args):
        '''Create section object from arguments'''
        raise NotImplementedError

    def create_sections(self, *args) -> list:
        '''Create section objects'''
        raise NotImplementedError
    
    def size(self) -> int:
        '''Returns total sections'''
        return len(self.sections)

    def set_sections(self, sections) -> None:
        '''Overide section objects with list of section objects'''
        if not self.contains_sections(sections):
            raise TypeError("sections contain non Section objects")
        self.sections = list(sections)

    def get_sections(self) -> list:
        '''Returns list of section objects'''
        return self.sections

    def section_qualify(self, section_obj) -> bool:
        '''Checks if section object qualify to be added to Container'''
        if not isinstance(section_obj, Section):
            raise TypeError("section_obj should be of type Section", 
            type(section_obj))
        # all section objects qualify by default
        return True


    def add_section(self, section_obj) -> bool:
        '''Add section object
        section_obj - section object to add'''
        if not isinstance(section_obj, Section):
            raise TypeError("section_obj should be of type Section", 
            type(section_obj))
        if self.section_qualify(section_obj):
            self.sections.append(section_obj)
            return True
        return False

    def filter_sections(self, sections, function) -> list:
        '''Filter section objects based on function'''
        if not self.contains_sections(sections):
            raise TypeError("sections contain non Section objects")
        assert callable(function), type(function) + "is not callable"
        return list(filter(function, sections))

    def filter_qualify_sections(self) -> list:
        '''Filter section objects based on function'''
        return self.filter_sections(self.sections, self.section_qualify)

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


    def __key(self) -> int:
        return super().__hash__()

    def __iter__(self):
        self.__sections_iter = iter(self.sections)
        return self.__sections_iter

    def __next__(self):
        return next(self.__sections_iter)

    def __len__(self, /) -> int:
        return self.size()

    def __bool__(self, /):
        return self.size() > 0
    
    def __getitem__(self, key) -> Section:
        return self.sections[key]

    def __contains__(self, key, /) -> bool:
        return key in self.sections
        

if __name__ == "__main__":
    container_obj = Container([Section("name")])
    text = "abcdefghij"
    for item in container_obj.filter_qualify_sections():
        print(item)
    print("finished", len(container_obj))
