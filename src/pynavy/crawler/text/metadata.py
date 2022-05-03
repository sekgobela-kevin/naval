
class Metadata():
    '''Defines extra data to be stored on objects'''
    def __init__(self, metadata={}):
        self.metadata = metadata

    def get_metadata(self) -> dict:
        '''Returns copy of metadata'''
        return self.metadata.copy()

    def set_metadata(self, metadata) -> None:
        '''Overide metadata dictionary with argument'''
        if isinstance(metadata, dict):
            self.metadata = metadata
        else:
            raise ValueError

    def add_data(self, key, value):
        '''Add item to metadata'''
        self.metadata[key] = value

    def get_data(self, key):
        '''Access item in metadata'''
        return self.metadata[key]

    def remove_data(self, key):
        '''Removes item in metadata'''
        del self.metadata[key]

    def data_exists(self, key):
        '''Checks if key exists in metadata'''
        return key in self.metadata

    def get_metadata_size(self):
        '''Returns the size of metadata'''
        return len(self.metadata)

    def clear_metadata(self):
        '''Clears all data in metadata'''
        self.metadata.clear()
    
