from __future__ import with_statement
from jira import JIRA
import json, sys, traceback, yaml

# TODO move to own place
def check_jira_server(server):
  try:
    return JIRA(server)
  except:
    return None

def validate_config(config_json):
  try:
    assert "server" in config_json # config must have server specified
    assert check_jira_server(config_json["server"]) # specified server must be valid
   
    assert "name" in config_json # config must have a name specified
    assert config_json["name"] # name must be non-empty

    assert "project_key" in config_json # config must have a project key specified
    assert config_json["project_key"] # project key must be non-empty

    assert "epic_fields" in config_json # config must have epic field block specified
    epic_json = config_json["epic_fields"]
    assert "summary" in epic_json # config must have an epic summary specified
    assert epic_json["summary"] # epic summary must be non-empty

    assert "description" in epic_json # config must have an epic description specified
    assert epic_json["description"] # epic_description must be non-empty

    assert "issues_to_create" in config_json # config must have a list of issues specified
    assert len(config_json["issues_to_create"]) > 0 # list of issues must be non-empty

    for issue_json in config_json["issues_to_create"]:
      assert "summary" in issue_json # each issue must have a summary specified
      assert "description" in issue_json # each issue must have a description specified
      if "assignee" in issue_json:
        assert "name" in issue_json["assignee"] # if assignee is specified, must have a field called 'name' insde
        

  except AssertionError:
    print "Config did not pass validation:"
    _, _, tb = sys.exc_info()
    traceback.print_tb(tb) # Fixed format
    tb_info = traceback.extract_tb(tb)
    filename, line, func, text = tb_info[-1]
    return False
  return True


def load_config(path_to_config):
  loaded = None
  with open(path_to_config, "r") as f:
    config_json = json.load(f)
    if validate_config(config_json):
      loaded = LoadedConfig(config_json)
  return loaded

class LoadedConfig:
  def __init__(self, input_dict):
    self.server = input_dict['server']
    self.name = input_dict['name']
    self.issues = [ConfigIssue(data) for data in input_dict['issues_to_create']]
    self.project_key = input_dict['project_key']
    self.raw_data = input_dict
  def get_epic_fields(self, name=""):
    return get_interp_data_helper(self.raw_data["epic_fields"], name=name)

class ConfigIssue:
  def __init__(self, issue_dict):
    self.data = issue_dict

  def get_interp_data(self, name="", epic_key=""):
    return get_interp_data_helper(self.data, name, epic_key)


def get_interp_data_helper(data, name="", epic_key=""):
  if isinstance(data, str) or isinstance(data, unicode):
    return interp_string(data, name, epic_key)
  new_dict = dict()
  for (k,v) in data.iteritems():
    # if key ends with gebsun_checklist, convert to gebsun checklist format (https://marketplace.atlassian.com/plugins/com.gebsun.plugins.jira.issuechecklist/cloud/overview)
    if k.endswith(".gebsun_checklist") and isinstance(v, list):
      checklist_dict = { "items": [ { "text": item.replace("{{name}}", name).replace("{{epic_key}}", epic_key) } for item in v ] }
      new_dict[k[:-len(".gebsun_checklist")]] = yaml.safe_dump(checklist_dict, default_flow_style=False)
    elif isinstance(v, dict):
      new_dict[k] = get_interp_data_helper(v, name, epic_key)
    elif isinstance(v, list):
      new_dict[k] = [get_interp_data_helper(i, name, epic_key) for i in v]
    else:
      new_dict[k] = interp_string(v, name, epic_key)
  return new_dict

def interp_string(in_str, name, epic_key):
  return in_str.replace("{{name}}", name).replace("{{epic_key}}", epic_key)

