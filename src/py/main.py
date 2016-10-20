from __future__ import with_statement
from jira import JIRA
import argparse, getpass
from config.configs import load_config

def get_authed_jira(server, username, password):
  return JIRA(server, basic_auth=(username, password))

def run_with_client(jira_client, config, eng_name):
  project = jira_client.project(config.project_key)
  
  data = config.get_epic_fields(name=eng_name)
  data["project"] = project.key
  data["issuetype"] = {"name": "Epic"}
  new_epic = jira_client.create_issue(fields=data)

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
