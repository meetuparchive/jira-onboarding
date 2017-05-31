from __future__ import with_statement
from validation.validation import validate_config

import json, yaml

## Load a config from filepath
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
  def get_epic_fields(self, name="", date=""):
    return get_interp_data_helper(self.raw_data["epic_fields"], name=name, date=date)

class ConfigIssue:
  def __init__(self, issue_dict):
    self.data = issue_dict

  def get_interp_data(self, name="", epic_key="", date=""):
    return get_interp_data_helper(self.data, name, epic_key, date)


def get_interp_data_helper(data, name="", epic_key="", date=""):
  if isinstance(data, str) or isinstance(data, unicode):
    return interp_string(data, name, epic_key, date)
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
      new_dict[k] = interp_string(v, name, epic_key, date)
  return new_dict

def interp_string(in_str, name, epic_key, date):
  return in_str.replace("{{name}}", name).replace("{{epic_key}}", epic_key).replace("{{date}}", date)
