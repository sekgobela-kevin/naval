from io import BytesIO, IOBase, StringIO
import os
import json
from naval.parse import Parse_Base
import naval


# setup file paths to use later
pdf_file_path = os.path.join("files", "sample_file.pdf")
html_file_path = os.path.join("files", "sample_file.html")
text_file_path = os.path.join("files", "sample_file.txt")
json_file_path = os.path.join("files", "sample_file.json")




class Parse_Json(Parse_Base):
    '''Parses json from parse'''
    # always try to provide content type
    # this will be useful when registering the class
    content_type = "text/json"
    
    def __init__(self, fetch_obj) -> None:
        super().__init__(fetch_obj)

    def create_doc(self) -> dict:
        '''Loads Json and return the results'''
        # the results will be stored at self.doc
        return json.loads(self.fetch_obj.read())

    def text_to_file(self):
        '''Extract text and store it to self.text_file'''
        replaced_chars = "()[]{}"
        # self.doc is return value of  .create_doc()
        new_json = json.dumps(self.doc, indent=2, separators=("\t", "\t"))
        for replaced_char in replaced_chars:
            new_json = new_json.replace(replaced_char, "")
        self.text_file.write(new_json)

    def html_to_file(self):
        '''Extract html and store it to self.html_file'''
        self.html_file.write(f"<pre>{self.get_text()}</pre>")

# create fetch object
fetch_obj = naval.create_fetch_object(json_file_path)
# fetch_obj.request() will be called internally
parse_obj = Parse_Json(fetch_obj)
text = parse_obj.get_text()
#print(text)

