from io import BytesIO, StringIO
import os
import naval


pdf_file_path = os.path.join("files", "sample_file.pdf")
html_file_path = os.path.join("files", "sample_file.html")
text_file_path = os.path.join("files", "sample_file.txt")


html = '''
    <div>
        <p> This is html paragraph</p>
        <p> This is another html paragraph</p>
    <div>
'''

# Extract text from html
text = naval.extract_text(html, source_locates_data=False, content_type="html")
#print(text)


# or you could do manually download webpage into memory file
def download_and_extract_text(url):
    file = BytesIO()
    naval.download(url, file)
    file.seek(0)
    webpage_html = file.read().decode()
    # now extract text from the html
    return naval.extract_text(webpage_html, source_locates_data=False,
    content_type="html")

# now you can use the function obove
text = download_and_extract_text("http://example.com/")
#print(text)

# downloads and extract text from webpage
# same as download_and_extract_text("http://example.com/")
text = naval.extract_text("http://example.com/")
#print(text)

# you can also use file path instead of url
# this will print text of pdf file
text = naval.extract_text(pdf_file_path)
#print(text)

# extract from pdf file located on web
#text = naval.extract_text("http://example.com/file.pdf",content_type="pdf")
#print(text)


# extract text from pdf file object
with open(pdf_file_path, "rb") as file_object:
    # content_type can be ommited(provide it for memory files)
    text = naval.extract_text(file_object, content_type="pdf")
    file_object.close()
#print(text)


# extract_html() behave same as extract_text()
# they just differ in their outputs

# -----------------------------------------------
# html and text could also be extracted to files
# -----------------------------------------------

# extract text from pdf to file in path
naval.extract_text_to_file(html_file_path, "html_output.txt")
# extract text into file in memory
file_object = StringIO()
naval.extract_text_to_file(html_file_path, file_object)


# extract html from pdf to file in path
naval.extract_html_to_file(pdf_file_path, "output.html")
# extract html into file in memory
file_object = StringIO()
naval.extract_html_to_file(pdf_file_path, file_object)



######################
## SOME FUN ##########
######################

def extract_texts(*args):
    texts = []
    for arg in args:
        texts.append(naval.extract_text(arg)) 
    return texts

texts = extract_texts(
    "https://www.google.com/", 
    "https://www.example.com/"
)
#print(texts)
