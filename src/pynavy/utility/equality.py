
class Equality():
    '''Provide implementation for __eq__() and __hash__() for
    other classes.'''
    def __key(self) -> int:
        return super().__hash__()

    def __eq__(self, other, /):
        return self.__key() == hash(other)
    
    def __ne__(self, other, /):
        return self.__key() != hash(other)

    def __hash__(self) -> int:
        return self.__key()
