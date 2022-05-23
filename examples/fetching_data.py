from io import BytesIO
from pynavy.crawler import Fetch

# Fetch class is used to create object for fetching data
# Data can be fetched from url, file path or file like objects
Fetch("http://example.com/")
Fetch("file.pdf")
Fetch(BytesIO(b"some bytes"))



# fetch object methods and attributes
fetch_obj = Fetch("http://example.com/")
# returns the url "http://example.com/" 
fetch_obj.get_source()
# returns file that stores fetched data
fetch_obj.get_file()
# returns copy of file that stores fetched data
fetch_obj.get_file_copy()
# checks file is empty(one returned by get_file())
# use it to check if data was written
fetch_obj.is_empty()
# direcly perfoms request and returns data
# data is never written to file after being received
fetch_obj.fetch()
# reads data from from file(one returned by get_file())
# same arguments as file.read()
fetch_obj.read()
# fetches data from the url to file(one returned by get_file())
# it performs request and writes to the file
fetch_obj.fetch_to_disc()
# fetches data from url by calling fetch_to_disc()
# only fetches if not already fetched/data not available
# wont fetch data if called repeately
fetch_obj.request()
# closes the file
fetch_obj.close()



# some cool functions using fetch object
def download_webpage(url):
    '''Example that download webpage data'''
    fetch_obj = Fetch(url)
    # dont forget to request for data
    # error will be raised if it fails to fetch data
    fetch_obj.request()
    return fetch_obj.read()

def read_file(file_path):
    fetch_obj = Fetch(file_path)
    # no need to request
    # fetch_obj.get_file() points to file in path
    return fetch_obj.read()

def read_file_like_obj(file_obj):
    # file like object is also supported
    fetch_obj = Fetch(file_obj)
    # fetch_obj.get_source() would filename of file_obj
    # or automatically generated with pattern "unknown_source_*"
    return fetch_obj.read()
