from io import BytesIO
import os

import naval
from naval import sources


# creates 'downloads' folder in same dir
folder_path = os.path.split(os.path.abspath(__file__))[0]
downloads_path = os.path.join(folder_path, "downloads")
if not os.path.exists(downloads_path):
    os.makedirs(downloads_path)



# downloads webpage into 'webpage.html'
naval.download("http://example.com/", os.path.join(downloads_path,"webpage.html"))

# download into file like object
# download() works for both file path and file like object
bytes_file = BytesIO()
naval.download("http://example.com/", bytes_file)


# download webpages at example.com and google.com
# files will be written to "downloads" folder
# "downloads" can be any directory
# "http://example.com/" will result file named http_example.com.html
naval.download_all(["http://example.com/", "http://google.com/"], downloads_path)

# downloads webpages from urls of html
# extract_html() extract html from webpage in the url
html = naval.extract_html("http://google.com/")
# not all urls from html will be valid in their own
urls = [url for url in sources.get_urls_from_html(html) if sources.is_url(url)]
# the first are fine
naval.download_all(urls[:3], downloads_path)
