import os, sys

def get_project_dir():
    '''Return project root directory path'''
    # slit name of module by path seperator
    split_path = os.path.abspath(__file__).split(os.sep)
    # remove folder name and module name part
    split_path = split_path[0:len(split_path)-2]
    # join back the split portions to create folder path
    return os.sep.join(split_path) + os.sep

def add_to_path(directory):
    '''Adds directory to sys path'''
    assert os.path.isdir(directory), directory
    sys.path.append(directory)
    assert directory in  sys.path

def add_project_folder_to_path(*args):
    '''Adds directory in project to path'''
    folder_path = os.path.join(get_project_dir(), *args)
    add_to_path(folder_path)


# adds project source dir to system path
# tests need access to naval package
# unittest seems not to provide that
add_project_folder_to_path("source")
add_project_folder_to_path("samples")
add_project_folder_to_path("")

