from __future__ import with_statement
from jira import JIRA
import getpass
import json
import os

class LoadedConfig:
  def __init__(self, input_dict):
    self.name = input_dict[u'name']
    self.issues = input_dict[u'issues_to_create']
    self.raw_data = input_dict

def load_configs(directory):
  filenames = ["%s/%s" % (directory, name) for name in os.listdir(directory) if not name.startswith(".")]
  loaded = []
  for fn in filenames:
    with open(fn, "r") as f:
      loaded.append(LoadedConfig(json.load(f)))
  return loaded

def get_authed_jira(server, username, password):
  return JIRA(server, basic_auth=(username, password))

def run_with_client(jira_client, config):
  eng_name = raw_input("What is the name of the Engineer we are onboarding? ")
  project = jira_client.project("EOT")
  summary = "Onboarding %s" % eng_name
  description = "Tasks to complete in the onboarding process for %s" % eng_name
  
  # TODO custom fields come from custom impl?
  new_epic = jira_client.create_issue(\
    project=project.key,\
    summary=summary,\
    description=description,\
    customfield_10004=summary,\
    issuetype={'name': 'Epic'})

  for issue in config.issues:
    data = issue
    data["project"] = project.key
    data["customfield_10002"] = new_epic.key
    data["issuetype"] = {"name": "Task"}

    print "Creating issue %s" % issue
    task = jira_client.create_issue(fields=data)
    print "Done"
    print

def main():
  print "Please provide Jira server to use and authentication:"
  server = raw_input("Server (ex. http://jira.atlassian.com): ")
  username = raw_input("Username: ")
  password = getpass.getpass("Password: ")

  config_to_use = None
  configs = load_configs("config")
  print "Choose a config to use:"
  for i,c in enumerate(configs):
    print "%s) %s" % (i+1, c.name)
  raw_choice = raw_input("Enter the number of the config you wish to use: ")
  try:
    config_to_use = configs[int(raw_choice) - 1]
  except:
    print "Invalid choice"
    exit(-1)

  jira_client = None
  try:
    jira_client = get_authed_jira(server, username, password)
  except:
    print "Invalid authentication provided for Jira"
    exit(-1)

  run_with_client(jira_client, config_to_use)

if __name__ == "__main__":
  main()
