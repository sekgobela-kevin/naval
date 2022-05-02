import sys
import os

def src_to_path(module_file, *sub_folders):
    ''' Locates src/ folder with sub_folders and add it to path.
        This seems to be the only way to access modules in src/.
    '''
    # find absolute path of folder containing module
    module_folder = os.path.dirname(os.path.abspath(__file__))
    # remove part after /tests
    # its possible to miss and match wrong folder test/ folder
    project_path = module_folder[:module_folder.rindex(os.path.join("tests"))] 
    assert os.path.exists(project_path), project_path + " does not exists"
    # add folder with module to path
    dest_path = os.path.join(project_path, "src", *sub_folders)
    assert os.path.exists(dest_path), dest_path + " does not exists"
    sys.path.append(dest_path)


if __name__ == "__main__":
    src_to_path(__file__, "..", "tests")