from __future__ import with_statement
from jira import JIRA
import argparse, getpass, json, os, sys, traceback

class LoadedConfig:
  def __init__(self, input_dict):
    self.server = input_dict['server']
    self.name = input_dict['name']
    self.issues = [ConfigIssue(data) for data in input_dict['issues_to_create']]
    self.project_key = input_dict['project_key']
    self.raw_data = input_dict

  def get_interp_field(self, field, name=""):
    return self.raw_data[field].replace("{{name}}", name)

class ConfigIssue:
  def __init__(self, issue_dict):
    self.data = issue_dict

  def get_interp_data(self, name="", epic_key=""):
    return get_interp_data_helper(self.data, name, epic_key)


def get_interp_data_helper(data, name="", epic_key=""):
  new_dict = dict()
  for (k,v) in data.iteritems():
    if isinstance(v, dict):
      new_dict[k] = get_interp_data_helper(v, name, epic_key)
    else:
      new_dict[k] = v.replace("{{name}}", name).replace("{{epic_key}}", epic_key)
  return new_dict

def validate_config(config_json):
  try:
    assert "server" in config_json # config must have server specified
    assert check_jira_server(config_json["server"]) # specified server must be valid
   
    assert "name" in config_json # config must have a name specified
    assert config_json["name"] # name must be non-empty

    assert "project_key" in config_json # config must have a project key specified
    assert config_json["project_key"] # project key must be non-empty

    assert "epic_summary" in config_json # config must have an epic summary specified
    assert config_json["epic_summary"] # epic summary must be non-empty

    assert "epic_description" in config_json # config must have an epic description specified
    assert config_json["epic_description"] # epic_description must be non-empty

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

def check_jira_server(server):
  try:
    return JIRA(server)
  except:
    return None

def get_authed_jira(server, username, password):
  return JIRA(server, basic_auth=(username, password))

def run_with_client(jira_client, config, eng_name):
  project = jira_client.project(config.project_key)
  
  # TODO custom fields come from custom impl?
  new_epic = jira_client.create_issue(\
    project=project.key,\
    summary=config.get_interp_field("epic_summary", name=eng_name),\
    description=config.get_interp_field("epic_description", name=eng_name),\
    customfield_10004=config.get_interp_field("epic_summary", name=eng_name),\
    issuetype={'name': 'Epic'})

  for issue in config.issues:
    data = issue.get_interp_data(name=eng_name, epic_key=new_epic.key)
    data["project"] = project.key
    data["issuetype"] = {"name": "Task"}

    print "Creating issue %s" % data["summary"]
    task = jira_client.create_issue(fields=data)
    print "Done"
    print

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--path_to_config", required=True, help="Path to configuration file to use")
  parser.add_argument("--validate", action="store_true", help="Only perform validation on config, don't execute")
  args = parser.parse_args()
  
  # load config, and validate
  loaded_config = load_config(args.path_to_config)
  if not loaded_config:
    print "Could not load config at %s" % args.path_to_config
    exit(-1)

  if args.validate:
    # if we are only validating our config, just bail here
    print "The provided config file is valid!"
    exit()

  print "Using %s configuration on %s jira instance" % (loaded_config.name, loaded_config.server)

  print "Please provide Jira authentication for %s:" % loaded_config.server
  username = raw_input("Username: ")
  password = getpass.getpass("Password: ")

  jira_client = None
  try:
    jira_client = get_authed_jira(loaded_config.server, username, password)
  except:
    print "Invalid authentication provided for Jira"
    exit(-1)

  eng_name = raw_input("What is the name of the person we are onboarding? ")
  run_with_client(jira_client, loaded_config, eng_name)

if __name__ == "__main__":
  main()
