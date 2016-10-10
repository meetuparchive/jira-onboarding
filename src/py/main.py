from jira import JIRA
import getpass

def get_authed_jira(server, username, password):
  return JIRA(server, basic_auth=(username, password))

def run_with_client(jira_client):
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

  # create issues to go along with it
  task = jira_client.create_issue(\
    project=project.key,\
    summary="Deeper Dive Training",\
    description="Get Deeper Dive Training",\
    issuetype={'name': 'Task'},\
    customfield_10002=new_epic.key)
  jira_client.assign_issue(task, "jake")

def main():
  print "Please provide Jira server to use and authentication:"
  server = raw_input("Server (ex. http://jira.atlassian.com): ")
  username = raw_input("Username: ")
  password = getpass.getpass("Password: ")

  jira_client = None
  try:
    jira_client = get_authed_jira(server, username, password)
  except:
    print "Invalid authentication provided for Jira"
    exit(-1)

  run_with_client(jira_client)

if __name__ == "__main__":
  main()
