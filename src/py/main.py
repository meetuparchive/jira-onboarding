from jira import JIRA
import getpass

def get_authed_jira(server, username, password):
  return JIRA(server, basic_auth=(username, password))

def main():
  print "Please provide Jira server to use and authentication:"
  server = raw_input("Server (ex. http://jira.atlassian.com): ")
  username = raw_input("Username: ")
  password = getpass.getpass("Password: ")

  try:
    jira_client = get_authed_jira(server, username, password)
  except:
    print "Invalid authentication provided for Jira"
    exit(-1)

if __name__ == "__main__":
  main()
