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
    # .request() is requests for data
    fetch_obj.request()
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
# here fetch obect is created from url
fetch_obj = Fetch("http://example.com/")
# and from file object
fetch_obj = Fetch(BytesIO(b"some bytes"))

# specified content type as pdf(useful when parsing)
fetch_obj = Fetch(pdf_file_path)
print(fetch_obj.get_content_type())
# application/pdf

# source_locates_data prevent html from being seen as url
# our html is our content(data) not resource locator(file path, url, etc)
html = "<p> this is html paragraph</a>"
# its also worth to provide content type(useful when parsing)
fetch_obj = Fetch(html, source_locates_data=False, content_type="text/html")
# always call .request() else fetch object wont contain data
fetch_obj.request()
print(fetch_obj.read())
# b'<p> this is html paragraph</a>'





##################################
#    YOU MAY FIND THIS USEFUL    #
##################################

# fetch object methods and attributes
fetch_obj = Fetch("http://example.com/")

# performs request for data
# relevant for urls or data located on web
# call it everytime to avoid problems
# it wont request if data is already available
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
    # error may be raised if it fails to fetch data
    fetch_obj.request()
    #fetch_obj.get_file().seek(0)
    # no need to seek the file
    return fetch_obj.read()

webpage_html = download_webpage("http://example.com/")
#print(webpage_html)


def read_file(file_path):
    fetch_obj = Fetch(file_path)
    fetch_obj.request()
    return fetch_obj.read()

pdf_bytes = read_file(pdf_file_path)
#print(pdf_bytes)


def read_file_like_obj(file_obj):
    # file like object is also supported
    fetch_obj = Fetch(file_obj)
    fetch_obj.request()
    return fetch_obj.read()


file_obj = BytesIO(b"sequence of bytes")
read_bytes = read_file_like_obj(file_obj)
#print(read_bytes)
