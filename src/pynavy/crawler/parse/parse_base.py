from ...utility.container import Container
from ..fetch.fetch_base import Fetch_Base

class Parse_Base():
    '''Base class for parsing fetch object into text, html or 
    container(sections)'''
    def __init__(self, fetch_obj: Fetch_Base) -> None:
        self.fetch_obj = fetch_obj
        self.fetch_obj.request()
    
    def to_text(self) -> str:
        '''Retuns text version of fetch object'''
        raise NotImplementedError

    def to_html(self) -> str:
        '''Retuns html version of fetch object'''
        raise NotImplementedError

    def to_container(self) -> Container:
        '''Retuns fetch object represented as container'''
        raise NotImplementedError

    @staticmethod
    def text_to_container(text) -> Container:
        '''Converts text to container(sections)'''
        pass

    @staticmethod
    def html_to_container(text) -> Container:
        '''Converts text to container(sections)'''
        pass
    
