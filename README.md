# Pynavy search
> simple small search engine in Python
## Description
Pynavy search is a simple search engine for searching through files and webpages with Python.
The 'Py' come from 'Python" language with navy named from [Datanavy search](https://www.datanavy.site).
Datanavy search was written also written in Python using Spacy, Numpy and other libraries.  

## About Datanavy search
Datanavy search was intended for learning Python back in 2021.
It included both code for searching, crawling and displaying results in browser.
Crawling was done with requests, beutifulsoup, Pdfminer.six, pydocx and pypdf for supporting different formats.
Text proccessing was handled by NLTK and Spacy frameworks.
Search portion was using Numpy for working with indexes(numbers) generated from indexes of Spacy tokens.  

For server side, it was using Flask due its simplicity and Javascript, CSS and HTML for displaying data 
in browser. It was hosted in [datanavy.site](https://www.datanavy.site/) at 
[pythonanywhere.com](https://www.pythonanywhere.com/) until
being shutdown. It was challenging when creating the search engine especially client-side(browser) since I
had no knowledge of client-server programming including HTTP.  

It functioned as expected and its speed was on expectations based on how I wanted it to be. It used a lot 
hard-drive memory due to serialisation Spacy doc objects. It was fast but not fast as you would expect search
engine to be. Search code wasnt optimised and no indexes were saved for later use. Indexes needed to be created
everytime searching a document which was slowing down searching. Spacy was also slow when proccessing text
even if its powerful featuring AI.

Client side libraries for Datanavy search include W3.CSS, W3.JS, AngularJS and JQuery  
Server-side libraries included Spacy, NLTK, Numpy, Beautysoup, Pydocx, Pypptx, Pdfminer.six and Flask.

> Datanavy search repo is private.
  
> Pynavy search is public version of Datanavy search

## About Pynavy search
Pynavy search uses code from Datanavy search but the code refactored and modified for easy maintainace.
Pynavy search doesnt include code for generating webpages but searching will be conducted through command-line.
Creating webpages would require setting up servers and creating html files which can be time consuming.
It will also require JavaScript which would add more layer of development on top creating the search engine.
The repository will only contain enough to create an executable that allows searching with commands like
```bash pynavy search --query "food chain"```.  

Its much easy create command-line interface than web-server interface which requires lot of configuarations and
installing more softwares. When developing Datanavy search, lot of time was spent on client side learning
how to use JS and CSS frameworks other than the search code. More time was supposed to be used on Python but ended
stuck on client-server communication. That was bad but introdused me how web technologies work together until
webpage is rendered to the client.  

Displaying search results on web can be done by seperate repository using maybe React/Bootstrap. Advantage is that
it could be used by Pynavy, Datanavy and also Pynavy search unlike the one included in Datanavy search. One thing
to do is not to repeat the same mistakes in Datanavy search. Starting to code without planning on how different
parts work together would bring problems that may require source code rewrite.
> related to [Cnavy search](https://github.com/Sekgobela-Kevin/cnavy)

### Pynavy search structure
Pynavy is divided into portions that perform certain functions from crawling for text data to performing a
search. Search can be performed with something like ```bash _pynavy search --query "food chain"``` which returns results piped to _less_ or similar program. 
>Basic parts include Crawler, Resources and Search

#### Crawler
Crawler portion/package is responsible for extracting text data from files and webpages. 
The same code from Datanavy search will be used for locating resources and extracting text data from them.
Crawler responsibility is to locate resources(what to be searched) and then extract text data from them.
Resources could be files(pdf, .txt), webpages or any medium that can provide text data. 
> Datanvy search has enough for this portion

#### Resources
**Resources** portion
Angral is portion/package for managing resources including saving them to database and then retrieving them to
be searched or proccessed. Raw resources are just resources in their text form while proccessed resource include resource in proccessed form. Resources portion has purpose of storing and managing these resources to be accssed and searched. 
> Datanvy search is poor here(improvements needed)  

#### Search portion
**Search** portion is responsible for performing search including ranking results generating indexes, etc.
Proccessed resources from **Resources** portion will be used and then search results generated. This portion will
use same techniques from Datanavy search but more improvement will be added to improve performance.
> Datanvy search has lot of issues here(improvements needed)  

see [Python project structure](https://github.com/yngvem/python-project-structure) to understand project structure beyond the mentioned.  

## Usage
> Expected commands and functionality from completed project/executable

```bash pynavy search --query [query]```   - should search for _query_ and return results in command-line.  
```bash pynavy search --type [search type]``` - specifies type of search to use, [keywords] would use only keywords search.  

```bash pynavy search --max-results [int]``` - specifies maximum results to returned.  
```bash pynavy search --min-relevance [percents]``` - specifies minimum relevance to consider result as relevance. 
                                            - Results below this will be considered not relevant.  
  
```bash pynavy search --exclude [resource] --query [query]```   - excludes  resourse from being searched.  
```bash pynavy search --include [resource] --query [query]```   - includes  resourse to be searched.  
 
```bash pynavy resources --add [resource-locator]``` - Add resource from source(path, url, etc).  
```bash pynavy resources --add -text [text] -title [text]``` - Add text as resource and specify title of the text.  
 
```bash pynavy resources --proccess [resources]``` proccesses resources with XTess  
```bash pynavy resources --proccess all``` proccesses all added resources  
```bash pynavy resources --proccess -remove [resources]``` remove proccessed resource
 
```bash pynavy resources -stutus [resources]``` displays status of resource  


## Support
Feel free to open an issue or contact me on [kevinnoko23@gmail.com](mailto:kevinnoko23@gmail.com).  

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Make changes as you wish, you wont break anything.  
Also update tests to match latest changes.  

## Authors and acknowledgment
Project development just started, feel free to contribute.
> also checkout [Cnavy search(C++)](https://github.com/Sekgobela-Kevin/cnavy)

## Project status
Project developmet just started but thankfully, some portions will be taken from private project Datanavy search.
That would be speed development but wont be enough to complete the project. If you are a beginer in Python or programming you could just contribute, even myself I also a beginner.  

> Sometimes I will be working with [Cnavy search](https://github.com/Sekgobela-Kevin/cnavy)
