from io import BytesIO, StringIO
from pynavy import crawler

html = '''
    <div>
        <p> This is html paragraph</p>
        <p> This is another html paragraph</p>
    <div>
'''

# Extract text from html 
# not yet supported(support will be added)
print(crawler.extract_text(html, content_type="html"))

# or you could do manually download webpage html to memory file
file = BytesIO()
crawler.download("http://example.com/", file)
file.seek(0)
webpage_html = file.read().decode()
# now extract text from the html
print(crawler.extract_text(webpage_html, content_type="html"))

# downloads and extract text from webpage
print(crawler.extract_text("http://example.com/"))
# extract text from pdf in file
print(crawler.extract_text("path_to_file.pdf"))
# extract from pdf file located on web
print(crawler.extract_text("http://example.com/file.pdf"))

# extract text from pdf file object
file_object = BytesIO()
print(crawler.extract_text(file_object, content_type="pdf"))


# extract html from pdf and docx files
print(crawler.extract_html("path_to_file.pdf"))
print(crawler.extract_html("path_to_file.docx"))

# extract_html() behave same as extract_text()
# they just differ in their outputs

# -----------------------------------------------
# html and text could also be extracted to files
# -----------------------------------------------

# extract text from pdf to file in path
crawler.extract_text_to_file("path_to_file.pdf", "output.txt")
# extract text into file in memory
file_object = StringIO()
crawler.extract_text_to_file("path_to_file.pdf", file_object)


# extract html from pdf to file in path
crawler.extract_html_to_file("path_to_file.pdf", "output.html")
# extract html into file in memory
file_object = StringIO()
crawler.extract_html_to_file("path_to_file.pdf", file_object)
