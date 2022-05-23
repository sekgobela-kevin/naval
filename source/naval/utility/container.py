from .section import Section
from .metadata import Metadata
from .equality import Equality

class Container(Metadata):
    '''Class for representing container of section object'''
    def __init__(self, sections=[], metadata={}) -> None:
        '''
        sections [container] - container of section objects
        '''
        super().__init__(metadata)
        # specifies section class used by the container
        self._section_class = Section
        if not self.contains_sections(sections):
            raise TypeError("sections contain non Section objects")
        # stores section objects
        self.sections = list(sections)
        # iterator to section objects
        self.__sections_iter = iter(self.sections)
    
    def contains_sections(self, sections):
        '''Checks if items in container are section objects'''
        for section in sections:
            if not isinstance(section, self._section_class):
                return False
        return True
    
    def size(self) -> int:
        '''Returns total sections'''
        return len(self.sections)

    @classmethod
    def create_start_indexes(cls, container_size, section_size) -> list:
        '''Create end indexes\n
        container_size - size of container(str, list, tuple)\n
        section_size - size of each section to be sliced from container'''
        start_indexes = []
        for index in range(0, container_size, section_size):
            start_indexes.append(index) 
        return tuple(start_indexes)

    @classmethod
    def create_end_indexes(cls, container_size, section_size) -> list:
        '''Create start indexes\n
        container_size - size of container(str, list, tuple)\n
        section_size - size of each section to be sliced from container
        '''
        end_indexes = []
        for index in range(section_size, container_size, section_size):
            end_indexes.append(index) 
        # add last index if missing
        # only if last container_size is not zero
        if container_size>0 and (container_size not in end_indexes):
            end_indexes.append(container_size)
        return tuple(end_indexes)

    @classmethod
    def create_start_end_indexes(cls, container_size, section_size):
        '''Creates start and end indexes
        container_size - size of container in characters\n
        section_size - size of each section in characters
        '''
        assert isinstance(container_size, int), type(container_size)
        assert isinstance(section_size, int), type(section_size)
        start_indexes = cls.create_start_indexes(container_size, section_size)
        end_indexes = cls.create_end_indexes(container_size, section_size)
        start_end_indexes = map(lambda x,y: (x,y), start_indexes, end_indexes)
        return tuple(start_end_indexes)

    def create_section(self, container, start_end_index):
        '''Create section object\n
        container - container to be sliced with start_end_index\n
        start_end_index - start and end index to extract section container\n'''
        assert(isinstance(start_end_index, tuple))
        start, end = start_end_index
        if start > end:
            raise Exception(f"start_index({start}) is greater than \
            end_index({end}")
        # check if start_end_index is out of range
        if start < 0 or end > len(container):
            raise Exception(f"start_end_index({start_end_index} out range\
            to container of length {len(container)}")
        section_container = container[start:end]
        return self._section_class(section_container, start_end_index)

    def create_sections(self, container, max_section_size=None) -> list:
        '''Create section objects from container\n\n
        container - container to create section objects from\n
        max_section_size - maximum size of each section(last section may not be)'''
        assert isinstance(max_section_size, int) or max_section_size == None
        container_length = len(container)
        # calculate max_section_size if not provided
        if max_section_size == None:
            possible_section_size = 100000
            if container_length > possible_section_size:
                max_section_size = possible_section_size
            else:
                max_section_size = container_length
        # create start_end_indexes for container sections
        start_end_indexes = self.create_start_end_indexes(container_length, 
            max_section_size)
        sections = []
        for start_end_index in start_end_indexes:
            section_obj = self.create_section(container, start_end_index)
            sections.append(section_obj)
        return sections

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
        if not isinstance(section_obj, self._section_class):
            raise TypeError("section_obj should be of type Section", 
            type(section_obj))
        # all section objects qualify by default
        return True


    def add_section(self, section_obj) -> bool:
        '''Add section object
        section_obj - section object to add'''
        if not isinstance(section_obj, self._section_class):
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
    container = "abcdefghij"
    for item in container_obj.filter_qualify_sections():
        print(item)
    print("finished", len(container_obj))
