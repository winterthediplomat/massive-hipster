#!/usr/bin/python2
import jinja2
import json
from os import walk
from os.path import join
from collections import OrderedDict

class OrderedSet(object):
    """
    too lazy to include the activestate recipe (or switch to a better python version)
    """
    def __init__(self):
        self.data = OrderedDict()

    def union(self, newDict):
        for key in newDict:
            if key not in self.data:
              self.data[key]=key
        return self

    def keys(self):
        return self.data.keys()
    def values(self):
        return self.data.values()

def generate_page(data, pagename="books.html", templatename="template.html"):
    template = jinja2.Template(open(join("templates", templatename)).read())
    open(pagename, "w").write(template.render(
                                      title=(data["title"] if "title" in data else pagename.replace("./generated/", "").replace(".html", "")),
                                      headers=data["headers"],
                                      books=data["books"]))

def read_json(jsonpath):
    doc=json.load(open(jsonpath))
    #print doc
    #doc = map(dict, doc)
    #headers = (reduce(lambda thisset, listitem: thisset.union(listitem), doc, OrderedSet())).keys()
    for book in doc["list"]:
        for head in doc["headers"]:
            if head not in book:
                try:
                    book[head] = doc["defaults"][head]
                except KeyError:
                    book[head]="n/a"
    return {"title": doc["title"], "headers": doc["headers"], "books": doc["list"] }

if __name__=="__main__":
    for act_path, _, files in walk("./databases"):
        booktitles = []
        for file_ in files:
            print( file_ )
            data = read_json(join(act_path, file_)) 
            generate_page(data, join("./generated", file_.replace(".json", ".html")))
            booktitles.append({file_.replace(".json", "") : "<a href=\""+file_.replace(".json", ".html")+"\">"+data["title"]+"</a>"})

        #print [{file_.replace(".json", "") : "<a href=\""+file_.replace(".json", ".html")+"\">"+file_.replace(".json", "")+"</a>"} for file_ in files]
        generate_page({"headers": ("lists",),
                      "books": booktitles}, #[{file_.replace(".json", "") : "<a href=\""+file_.replace(".json", ".html")+"\">"+file_.replace(".json", "")+"</a>"} for file_ in files]},
                      "./generated/index.html", "index.html")    
