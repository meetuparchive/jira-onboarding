# jira-onboarding
Automated creation of a Jira board to track the onboarding process for new hires. Provide a config file of the format specified below, and the script takes care of the rest.

# running
To run, just clone this repo and run

`run.sh [path to config file]`

and then follow the prompts. You will be prompted to login with your Jira username and password.

# config files:
## example
### (core-eng.json)
	{
	  "server": "https://myserver.atlassian.net",
	  "name": "Core Engineering",
	  "project_key": "PK",
	  "epic_fields": {
		"summary": "Onboarding {{name}}",
		"description": "Tasks to complete in the onboarding process for {{name}}",
	  },
	  "issues_to_create": [
		{
		  "summary": "Deploy to production",
		  "description": "By the end of your first day, you should have code running in production!",
		},
		{
		  "summary": "Core Team Training",
		  "description": "Go through Core team training class",
		  "assignee": { "name" : "jake" }
		}
	  ]
	}

# dependancies
This is a self contained python script running in a virtualenv wrapped in a bash script.

The bash script downloads [virtualenv](https://virtualenv.pypa.io/en/stable/) and uses pip to install the python jira client inside.

This environment is used to execute a python script making use of the jira client, so no need to mess with the python install on your machine.

A config file similar to the one above is required to use, and a jira server which you have permission to access must be specified in it.
