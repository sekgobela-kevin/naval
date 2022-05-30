## naval

### Description
`naval` downloads, fetches and extract text, html from url, file path,
file object and more. Downloading(fetching) data from url will be handled
for you. `pdf`, `docx`, `pptx`, `html`, and `text` files are supported out of 
box.  

File can be from URL, file path, file object or even bytes. URL can point
to webpage instead of file e.g [google.com](https://google.com/) which
will be treated as html. Its all about file extensions, `file.html` will be
treated as html unless explicitly specified.

### Install
naval can be installed with pip  
```bash 
pip install navaly
```

### Usage
downloading from url:

```python
# download to file in path
naval.download("http://example.com/", "output.html")
naval.download("http://example.com/sample.pdf", "output.pdf")

# download to file like object
file_output = BytesIO()
naval.download("http://example.com/sample.pdf", file_output)

# download from multiple urls into folder
# html file will downloaded to 'downloads/' folder
urls = ["http://example.com/", "https://www.google.com/"]
naval.download_all(urls, "downloads")
```

Extract text and html
```python
# extract text from pdf, docx and pptx files
output_text = naval.extract_text("sample_file.pdf")
output_text = naval.extract_text("sample_file.pptx")
output_html = naval.extract_html("sample_file.docx")

# Extract from file like object
with open("sample_file.pdf", mode="rb") as file:
    output_text = naval.extract_text(input_file)

# extract to file(file path, file object)
naval.extract_text_to_file("sample_file.pdf", "output.txt")
naval.extract_html_to_file("sample_file.pdf", "output.html")

# string can passed directly
html = '''
<p> First paragraph </p>
<p> Second paragraph </p>
'''
output_text = naval.extract_text(html, source_locates_data=False, content_type="text/html")

# same with bytes
with open("sample_file.pdf", mode="rb") as file:
    pdf_bytes = file.read()
    output_html = naval.extract_html(pdf_bytes, source_locates_data=False, content_type="application/pdf")

```
> More examples can be found at `examples/` folder

### Support
Feel free to open an issue or contact me on [kevinnoko23@gmail.com](mailto:kevinnoko23@gmail.com).  

### Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
> Dont forget to update tests.  
