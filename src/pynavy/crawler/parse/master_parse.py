from typing import Dict, Set, Type

from .parse_base import Parse_Base
from .html_parse import HTML_Parse
from .docx_parse import DOCX_Parse
from .pptx_parse import PPTX_Parse
from .pdf_parse import PDF_Parse
from .text_parse import Text_Parse


class Master_Parse():
    '''Manages and simplifies interactions with parse classes'''
    # dictionary for storing map between fetch_obj exention and parse class
    # e.g {".txt": Parse_Base}
    # python-magic library could make things simpler by analysing bytes
    parse_classes: Set[Type[Parse_Base]] = set()

    @staticmethod
    def is_fetch_valid(parse_obj: Parse_Base) -> bool or Parse_Base:
        '''Checks if fetch object supported/valid based on its source.\n
        parse_obj - parse object with data to parse'''
        for parse_class in Master_Parse.parse_classes:
            if parse_class.is_fetch_valid(parse_obj):
                return True
        return False

    @staticmethod
    def parse_class_exists(parse_obj: Parse_Base) -> bool or Parse_Base:
        '''Checks if parse class for parse object exists\n
        parse_obj - parse object with data to parse'''
        return Master_Parse.is_parse_valid(parse_obj)

    @staticmethod
    def get_parse_class(fetch_obj: str) -> Type[Parse_Base]:
        '''returns parse class for fetch_obj if exists\n
        parse_obj - parse object with data to parse'''
        for parse_class in Master_Parse.parse_classes:
            # some fetch_objs arent supported by all parse classes
            try:
                if parse_class.is_fetch_valid(fetch_obj):
                    return parse_class
            except(ValueError, TypeError):
                continue
        raise Exception(f"parse class for fetch_obj with " +  
        f"source({fetch_obj.get_source()}) not found")

    @staticmethod
    def get_parse_object(fetch_obj: str, *args, **kwargs) -> Parse_Base:
        '''returns parse object for fetch_obj if parse class exists\n
        parse_obj - parse object with data to parse'''
        parse_class = Master_Parse.get_parse_class(fetch_obj)
        return parse_class(fetch_obj, *args, **kwargs)

    @staticmethod
    def get_text(fetch_obj: str, *args, **kwargs) -> Parse_Base:
        '''Returns text version of fetch object\n
        parse_obj - parse object with data to parse'''
        parse_object = Master_Parse.get_parse_object(fetch_obj)
        return parse_object.get_text(*args, **kwargs)

    @staticmethod
    def get_html(fetch_obj: str, *args, **kwargs) -> Parse_Base:
        '''Returns html version of fetch object\n
        parse_obj - parse object with data to parse'''
        parse_object = Master_Parse.get_parse_object(fetch_obj)
        return parse_object.get_html(*args, **kwargs)

    @staticmethod
    def get_text_file(fetch_obj: str, *args, **kwargs) -> Parse_Base:
        '''Returns file with text extracted from fetch_obj\n
        parse_obj - parse object with data to parse'''
        parse_object = Master_Parse.get_parse_object(fetch_obj)
        return parse_object.get_text_file_copy()

    @staticmethod
    def get_html_file(fetch_obj: str, *args, **kwargs) -> Parse_Base:
        '''Returns file with html extracted from fetch_obj\n
        parse_obj - parse object with data to parse'''
        parse_object = Master_Parse.get_parse_object(fetch_obj)
        return parse_object.get_htmlfile_copy()

    @staticmethod
    def register_parse_class(parse_class: Type[Parse_Base]) -> None:
        '''Registers class for parseing data from fetch_obj'''
        # parse_class needs to inherit Parse_Base
        if not issubclass(parse_class, Parse_Base):
            raise TypeError(f"parse_class subclass of Parse_Base",
            parse_class)
        Master_Parse.parse_classes.add(parse_class)
    
    @staticmethod
    def parse_class_registered(parse_class: Type[Parse_Base]) -> bool:
        '''Checks if parse class is registered'''
        # parse_class needs to inherit Parse_Base
        if not issubclass(parse_class, Parse_Base):
            raise TypeError(f"parse_class subclass of Parse_Base",
            parse_class)
        return parse_class in Master_Parse.parse_classes

    @staticmethod
    def deregister_parse_class(parse_class: Type[Parse_Base]) -> None:
        '''Registers class for parseing data from fetch_obj'''
        # parse_class needs to inherit Parse_Base
        if not issubclass(parse_class, Parse_Base):
            raise TypeError(f"parse_class subclass of Parse_Base",
            parse_class)
        if Master_Parse.parse_class_registered(parse_class):
            Master_Parse.parse_classes.remove(parse_class)

    @staticmethod
    def deregister_parse_classes():
        '''Deregisters parse class'''
        Master_Parse.parse_classes.clear()

# register parse classes
Master_Parse.register_parse_class(PDF_Parse)
Master_Parse.register_parse_class(DOCX_Parse)
Master_Parse.register_parse_class(PPTX_Parse)
Master_Parse.register_parse_class(HTML_Parse)
Master_Parse.register_parse_class(Text_Parse)
