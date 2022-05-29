from io import BytesIO, StringIO
import os
from naval.fetch import Fetch
from naval.parse import Parse
from naval import sources
import naval


# setup file paths to use later
pdf_file_path = os.path.join("files", "sample_file.pdf")
html_file_path = os.path.join("files", "sample_file.html")
text_file_path = os.path.join("files", "sample_file.txt")





def extract_text_from_fetch_object(fetch_object):
    if not isinstance(fetch_object, Fetch):
        err_msg = "fetch_object is not instance of Fetch class"
        raise Exception(err_msg, type(fetch_object))
    # this creates object for parsing data
    parse_obj = Parse(fetch_object)
    return parse_obj.get_text()


def extract_html_from_fetch_object(fetch_object):
    if not isinstance(fetch_object, Fetch):
        err_msg = "fetch_object is not instance of Fetch class"
        raise Exception(err_msg, type(fetch_object))
    # this creates object for parsing data
    parse_obj = Parse(fetch_object)
    return parse_obj.get_html()


# creates fetch object and request for data
fetch_object = Fetch(html_file_path)
fetch_object.request()
# let the function handle everything
text = extract_text_from_fetch_object(fetch_object)
#print(text)



def extract_text_from_file_path(file_path):
    if not sources.is_local_file(file_path):
        err_msg = f"file_path{file_path} does not look like file path"
        raise Exception(err_msg, type(file_path))
    fetch_obj = Fetch(file_path)
    # this creates object for parsing data
    parse_obj = Parse(fetch_obj)
    return parse_obj.get_text()

def extract_html_from_file_path(file_path):
    if not sources.is_local_file(file_path):
        err_msg = f"file_path{file_path} does not look like file path"
        raise Exception(err_msg, type(file_path))
    fetch_obj = Fetch(file_path)
    # this creates object for parsing data
    parse_obj = Parse(fetch_obj)
    return parse_obj.get_html()


text = extract_text_from_file_path(pdf_file_path)
#print(text)

# here html was extracted from pdf file
html = extract_html_from_file_path(pdf_file_path)
#print(html)



######################################################
#        FUNCTIONS YOU MAY FIND USEFUL               #
######################################################

# similar to creating directly from Fetch class
fetch_obj = naval.create_fetch_object(html_file_path)
# similar to creating directly from Parse class
parse_obj = naval.create_parse_object(fetch_obj)

# parse object can be created directly from file path
parse_obj = naval.create_parse_object(html_file_path)
# also works with url and file object
with open(html_file_path) as file:
    parse_obj = naval.create_parse_object(file)
    text = parse_obj.get_text()
    #print(text)


html = '''<div>
    <p> paragraph in div</p>
    <p> paragraph2 in div</p>
</div>'''
# text or bytes can also be passed directly
# source_locates_data=False allows to data direcly(without url or path)
# content_type specified the type of data in text or bytes
parse_obj = naval.create_parse_object(html, source_locates_data=False,
content_type="html")
#print(parse_obj.get_text())



# Works like charm
# Extracts text from html and pdf files
text = naval.extract_text(html_file_path)
# specify optional content type
text = naval.extract_text(pdf_file_path, content_type="pdf")


# Now extracts html
# naval.extract_text() takes same arguments as naval.extract_text()
# file object can also be passedinstead of file path
html = naval.extract_html(pdf_file_path)
#print(html)


# extract text from html into file
# file path, url could also be passed instead of file objetc
with StringIO() as file:
    naval.extract_text_to_file(html_file_path, file)
    file.seek(0)
    #print(file.read())

# the same applies to extarcting html to file
with StringIO() as file:
    naval.extract_html_to_file(pdf_file_path, file)
    file.seek(0)
    #print(file.read())
