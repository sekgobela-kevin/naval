import os
import re
import glob
import shutil
from os.path import normpath, basename


def cwd():
    '''Returns current working directory'''
    return os.getcwd()

def is_dir(path):
    '''Checks if path points to folder'''
    return os.path.isdir(path)

def create_dir(path):
    '''Creates directory if not yet existing'''
    if not is_dir(path):
        os.mkdir(path)

def delete_dir(path):
    '''Deletes directory'''
    if is_dir(path):
        try:
            shutil.rmtree(path)
            return True
        except PermissionError:
            return False

def rename_dir(old, new):
    '''Renames directory from old to new'''
    assert is_dir(old), f"{old} is not valid directory"
    os.rename(old, new)

def is_file_empty(path):
    '''Checks if file is empty'''
    return os.path.getsize(path) == 0

def is_file(path):
    '''Checks if path points to a file'''
    return os.path.isfile(path)

def create_file(path):
    '''Creates file'''
    file = open(path, 'w', encoding='utf-8')
    file.close()

def write_file(file_path, content):
    '''Writes into a file'''
    file = open(file_path, "w", encoding='utf-8')
    file.write(content)
    file.close()

def append_file(file_path, content):
    '''Appends content into file in path'''
    file = open(file_path, "a", encoding='utf-8')
    file.write(content)
    file.close()

def remove_file(path):
    '''Removes file in path'''
    try:
        os.remove(path)
        return True
    except PermissionError:
        return False
    except FileNotFoundError:
        return False

def file_read(file_path):
    '''Read contents of file'''
    file = open(file_path, "r", encoding='utf8')
    content = file.read()
    file.close()
    return content

def get_filename_extension(path):
    '''Returns filename with its extension'''
    return os.path.basename(path)

def get_file_extension(path):
    '''Returns extension of file'''
    base = get_filename_extension(path)
    return os.path.splitext(base)[1]

def get_filename(path):
    '''Returns filename without extension'''
    base = get_filename_extension(path)
    return os.path.splitext(base)[0]

def files_paths(folder_path, format_=None):
    '''Returns paths of files in path'''
    #file within function name is misleading
    files_paths = []
    if format_!=None:
        folder_path = os.path.join(folder_path,"*."+format_)
    else:
        folder_path = os.path.join(folder_path,"*")
    for file in glob.glob(folder_path):
        files_paths.append(file)
    return files_paths

def get_folders(folder_path):
    '''Returns folder in path'''
    assert is_dir(folder_path), f"'{folder_path}' is not a directory/folder"
    return [path for path in files_paths(folder_path) if is_dir(path)]

def delete_folder_contents(folder_path):
    '''Delete contents of folder'''
    folder_files_paths = files_paths(folder_path)
    for file_path in folder_files_paths:
        remove_file(file_path)

def get_valid_filename(s):
    '''Returns valid path version of argument'''
    s = str(s).strip()
    return re.sub(r'(?u)[^-\w.]', ' ', s)

def get_folder_name(path):
    '''Returns name of folder'''
    return basename(normpath(path))

if __name__ == "__main__":
    pass
