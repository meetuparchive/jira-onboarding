from jira import JIRA

## Return an instance of an authed jira client using provided server, username, and password
def get_authed_jira(server, username, password):
  return JIRA(server, basic_auth=(username, password))

## Check if a jira server can be resolved at all at the given server location - no auth
def check_jira_server(server):
  try:
    return JIRA(server)
  except:
    return None

