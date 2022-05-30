from io import BytesIO, IOBase, StringIO
import os, json
from naval.parse import Parse_Base
from naval.fetch import Fetch
import naval


# setup file paths to use later
pdf_file_path = os.path.join("files", "sample_file.pdf")
html_file_path = os.path.join("files", "sample_file.html")
text_file_path = os.path.join("files", "sample_file.txt")
json_file_path = os.path.join("files", "sample_file.json")


# follow examples/extending_parse.py
# for more on extending parse classes
class Parse_Json(Parse_Base):
    '''Parses json from parse'''
    # always try to provide content type
    # this will be useful when registering the class
    fetch_content_type = "application/json"
    
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



# let first deregister all existing parse classes
naval.deregister_parse_classes()

# error will be raised(no parse class)
#naval.create_parse_object(json_)

# same with Parse class(no parse class)
#parse_obj = naval.Parse(json_)

# methods including extract_text() wont work
# they depend on parse classes to parse data



################################
# LET REGISTER OUR PARSE CLASS #
################################

naval.register_parse_class(Parse_Json)

# let create parse objetct from .create_parse_object()
# and Parse class.
parse_obj = naval.create_parse_object(json_file_path)
parse_obj = naval.Parse(Fetch(json_file_path))
# realise that error wasnt raised


# parse class register and deregister functions
###############################################

# registers parse class
naval.register_parse_class(Parse_Json)
# deregisters parse class
naval.deregister_parse_class(Parse_Json)
# returns True if parse class is registered
naval.parse_class_registered(Parse_Json)
# returns refererance registered parse classes
naval.get_registered_parse_classes()
# dregistered all parse classes
naval.deregister_parse_classes()

# only deregisters parse classes passed
naval.deregister_parse_classes([Parse_Json])


# Let extract text from pdf file
naval.register_parse_class(Parse_Json)
text = naval.extract_text(json_file_path)
#print(text)
