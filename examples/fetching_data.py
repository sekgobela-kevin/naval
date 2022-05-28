from io import BytesIO
import os
from naval.fetch import Fetch

# setup file paths to use later
pdf_file_path = os.path.join("files", "sample_file.pdf")
html_file_path = os.path.join("files", "sample_file.html")
text_file_path = os.path.join("files", "sample_file.txt")




# let create function to download webpage
def download(url):
    # this only creates the object without fecthing data
    fetch_obj = Fetch(url)
    fetch_obj.request()
    fetch_obj.get_file().seek(0)
    # reads fetched data bytes
    return fetch_obj.read()

# let use the method to download webpage
webpage_html = download("http://example.com/")
#print(webpage_html)

# it can also work with file system
# Fetch class will take care of everything
pdf_bytes = download(pdf_file_path)


# our download method is doing well
# it could also handle file object
with open(pdf_file_path, "rb") as file:
    pdf_bytes = download(file)
    #print(pdf_bytes)

# Fetch class is used to create object for fetching data
# Data can be fetched from url, file path or file like objects
fetch_obj = Fetch(pdf_file_path)
fetch_obj = Fetch("http://example.com/")
fetch_obj = Fetch(BytesIO(b"some bytes"))



##################################
#    YOU MAY FIND THIS USEFUL    #
##################################


# fetch object methods and attributes
fetch_obj = Fetch("http://example.com/")

# performs request for data
# relevant for urls or data located on web
fetch_obj.request()

# returns the url "http://example.com/"
fetch_obj.get_source()

# returns refereance to file that stores fetched data
# remember to call .request() for urls else it will be empty
fetch_obj.get_file()

# returns copy of file that stores fetched data
fetch_obj.get_file_copy()

# checks file is empty(one returned by get_file())
# use it to check if data was written
fetch_obj.is_empty()

# directly perfoms request and returns data
# data is never written to file after being received
# but requires the source as argument
fetch_obj.fetch(fetch_obj.get_source())

# reads data from from file(one returned by get_file())
# same arguments as file.read()
# remeber to seek() on file
fetch_obj.read()


# this is the method that fetches data from source to file
# gets called by .request()
# requires source and file object as argument
file_obj = BytesIO()
fetch_obj.fetch_to_file(fetch_obj.get_source(), file_obj)

# closes any opened files
fetch_obj.close()



################################################
#    SOME COOL FUNCTIONS USING FETCH OBJECT    #
################################################

def download_webpage(url):
    '''Example that download webpage data'''
    fetch_obj = Fetch(url)
    # dont forget to request for data
    # error will be raised if it fails to fetch data
    fetch_obj.request()
    fetch_obj.get_file().seek(0)
    return fetch_obj.read()

webpage_html = download_webpage("http://example.com/")
#print(webpage_html)


def read_file(file_path):
    fetch_obj = Fetch(file_path)
    # no need to request
    # fetch_obj.get_file() points to file in path
    # dont forget to seek() to beginning
    fetch_obj.get_file().seek(0)
    return fetch_obj.read()

pdf_bytes = read_file(pdf_file_path)
#print(pdf_bytes)


def read_file_like_obj(file_obj):
    # file like object is also supported
    fetch_obj = Fetch(file_obj)
    # dont forget to seek to the beginning
    fetch_obj.get_file().seek(0)
    return fetch_obj.get_file().read()


file_obj = BytesIO(b"sequence of bytes")
read_bytes = read_file_like_obj(file_obj)
