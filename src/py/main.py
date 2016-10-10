from __future__ import with_statement
from jira import JIRA
import argparse, getpass, json, os

class LoadedConfig:
  def __init__(self, input_dict):
    self.server = input_dict[u'server']
    self.name = input_dict[u'name']
    self.issues = input_dict[u'issues_to_create']
    self.raw_data = input_dict

def load_config(path_to_config):
  loaded = None
  with open(path_to_config, "r") as f:
    loaded = LoadedConfig(json.load(f))
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
  parser = argparse.ArgumentParser()
  parser.add_argument("--path_to_config", required=True)
  args = parser.parse_args()

  loaded_config = load_config(args.path_to_config)
  if not loaded_config:
    print "Could not load config at %s" % args.path_to_config
    exit(-1)
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

  run_with_client(jira_client, loaded_config)

if __name__ == "__main__":
  main()
