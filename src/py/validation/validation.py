from jira_instance.jira_instance import check_jira_server
import sys, traceback

## Run validation checks on a given configuration json object
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
