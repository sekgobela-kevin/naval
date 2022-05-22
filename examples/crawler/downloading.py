from asyncio import streams
from io import BytesIO, StringIO

from pynavy.crawler import download
from pynavy.crawler import download_all
from pynavy.crawler import sources

import os

from pynavy.crawler.crawler import extract_html


# downloads webpage into 'webpage.html'
# any path path to file would work
# file does not need to exists
download("http://example.com/", "webpage.html")

# download into file like object
# download() works for both file path and file like object
bytes_file = BytesIO()
download("http://example.com/", bytes_file)


# download webpages at example.com and google.com
# files will be written to "downloads" folder
# "downloads" can be any directory
# "http://example.com/" will result file named http_example.com.html
download_all("downloads", ["http://example.com/", "http://google.com/"])

# download webpages from urls of html
# this good for downloading other webpages related to certain webpage
# extract_html() extract html from webpage in the url
html = extract_html("http://google.com/")
download_all("downloads", sources.get_urls_from_html(html))
