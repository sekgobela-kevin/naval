from io import BytesIO
import os

import naval
from naval import sources


# creates 'downloads' folder
downloads_path = "downloads"
if not os.path.exists(downloads_path):
    os.makedirs(downloads_path)




# downloads webpage into 'webpage.html'
naval.download("http://example.com/", os.path.join("downloads","webpage.html"))

# download into file like object
# download() works for both file path and file like object
bytes_file = BytesIO()
naval.download("http://example.com/", bytes_file)


# download webpages at example.com and google.com
# files will be written to "downloads" folder
# "downloads" can be any directory
# "http://example.com/" will result file named http_example.com.html
naval.download_all("downloads", ["http://example.com/", "http://google.com/"])

# downloads webpages from urls of html
# extract_html() extract html from webpage in the url
html = naval.extract_html("http://google.com/")
# not all urls from html will be valid in their own
urls = [url for url in sources.get_urls_from_html(html) if sources.is_url(url)]
# the first are fine
naval.download_all("downloads", urls[:3])
