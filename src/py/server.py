from klein import Klein
from twisted.web.template import Tag, Element, renderer, flattenString, tags, XMLFile
from twisted.python.filepath import FilePath

from config import configs
import json

def get_loader(template_name):
  return XMLFile(FilePath("templates/%s.xml" % template_name))

class Page(Element):
  @renderer
  def header(self, request, tag):
    return tag(Header())

class HomePage(Page):
  loader = get_loader("index")

class Config(Page):
  loader = get_loader("config")

  def __init__(self, config_data):
    self.config_data = config_data

  @renderer
  def config(self, request, tag):
    return item_to_tag(self.config_data.raw_data)

def item_to_tag(item):
  if isinstance(item, str) or isinstance(item, unicode):
    return tags.span(item)
  if isinstance(item, list):
    child_items = [tags.li(item_to_tag(i)) for i in item]
    return Tag("ol", children=child_items)
  if isinstance(item, dict):
    child_items = [Tag("li", children=[tags.span("%s: " % k), item_to_tag(v)]) for (k,v) in item.items()]
    return Tag("ul", children=child_items)

class Header(Element):
  loader = get_loader("header")

class JiraOnboardingWebImpl(object):
  app = Klein()

  @app.route('/')
  def land(self, request):
    return HomePage()

  @app.route('/upload', methods=['POST'])
  def upload(self, request):
    farray = request.args.get("datafile")
    if not farray:
      return "Must upload a file"
    if len(farray) > 1:
      return "Please only upload one file"
    f = farray[0]
    config = configs.load_config_from_string(f)
   
    if not config:
      return "not a valid config file"

    return Config(config)

if __name__ == "__main__":
  web = JiraOnboardingWebImpl()
  web.app.run('localhost', 8080)

