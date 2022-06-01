
import io

def is_file_object(source):
    '''Cheks if object is file like object'''
    # file objects inherits IOBase
    if isinstance(source, io.IOBase):
        return True
    elif hasattr(source, "write"):
        file_objs_attr = ["read", "writelines", "truncate", "seek", "closed"]
        # this will work for _TemporaryFileWrapper class
        # its returned by tempfile.TemporaryFile() on windows
        return all([hasattr(source, attr) for attr in file_objs_attr])
    return False

def is_binary(file_obj):
    '''Cheks if file object is in binary mode'''
    if not is_file_object(file_obj):
        raise TypeError("file_obj is not file like object", type(file_obj))
    else:
        return isinstance(file_obj.read(0), bytes)

def is_text(file_obj):
    '''Cheks if file object is in text mode'''
    return not is_binary(file_obj)

def get_file_object(file, **kwarg):
    '''Return file object from file path or anothe file object\n
    file - string file path or file like object\n
    kwarg - optional keywords arguments to pass to open()'''
    # file path could also be bytes
    # isinstance(file, str) will cause problems
    if not (is_file_object(file) or isinstance(file, str)):
        err_msg = "file should be str file path or file object"
        raise TypeError(err_msg, type(file))
    if isinstance(file, str):
        file_obj = open(file, **kwarg)
    else:
        file_obj = file
    return file_obj


def copy_file(src_file, dest_file):
    '''Copy file in from src_file to dest_file\n
    src_file - source string file path or file like object\n
    src_file - destination string file path or file like object'''
    try:
        # create file objects
        src_file_obj = get_file_object(src_file)
        # guess mode to open dest_file based on src_file_obj
        if is_binary(src_file_obj): dest_file_mode = "wb"
        else: dest_file_mode = "w"
        dest_file_obj = get_file_object(dest_file, mode=dest_file_mode)
        # seek to begining of files
        dest_file_obj.seek(0)
        src_file_obj.seek(0)
        # write source file into destination
        dest_file_obj.writelines(src_file)
        # close file if argument is not file like object
        # it makes no sense to close file like object arguments
        if not is_file_object(src_file):
            src_file_obj.close()
        if not is_file_object(dest_file):
            dest_file_obj.close()
        # users will close file objects themeselfs
    except Exception as e:
        # close files if there are errors
        try:
            src_file_obj.close()
            dest_file_obj.close()
        except UnboundLocalError:
            pass
        raise e
