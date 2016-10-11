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
