import os, sys

def get_project_dir():
    '''Return project root directory path'''
    # slit name of module by path seperator
    split_path =__file__.split(os.sep)
    # remove folder name and module name part
    split_path = split_path[0:len(split_path)-2]
    # join back the split portions to create folder path
    return os.sep.join(split_path) + os.sep

def add_project_source_to_path():
    '''Adds project source directory to path'''
    project_dir = get_project_dir()
    assert os.path.isdir(project_dir), project_dir
    sys.path.append(os.path.join(project_dir, "source"))

# adds project source dir to system path
# tests need access to pynavy package
# unittest seems not to provide that
add_project_source_to_path()
