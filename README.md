# jira-onboarding
Automated creation of a Jira board to track the onboarding process for new hires. Provide a config file of the format specified below, and the script takes care of the rest.

# running
To run, just clone this repo and run

`run.sh --path_to_config [path to config file]`

and then follow the prompts. You will be prompted to login with your Jira username and password.

## logging in
If you are having issues logging into Jira with a username and password (maybe you don't have a password because of SSO), follow the following steps:
- Go to https://meetup.atlassian.net/
- Click `Can't log in?` underneath the login box
- Type in your associated meetup email account and click `Send recovery link`
- Check your email for the recovery link. In this email look for `Alternatively, you can reset your password for your Atlassian account.` and click the link to reset your password. Don't click `Log in to my account`!! This will just log you in and not give you the chance to set a password
- Type in your new password and submit. Use this to log in!

# config files:
## validation
You can run validation on your config file (to make sure that necessary fields are present) by running

`run.sh --validate --path_to_config [path to config file]`

This will report an error if any required fields (such as server, name, project key, etc...) are not present.

This validation is also ran before running the script as normal, so this is more of a dry-run test.

Note that this will not catch ALL issues with your config, namely the presense of required custom fields that could be configured in the Jira instance you are using.  Validation currently does not check anything related to the Jira server beyond the existance of the server itself.
## variables
There are two variables you can include in your conf file, to hold things that you won't know ahead of time when writing the config. they are:
- `{{name}}`: represents the name of the person you are onboarding - you will be prompted to specify this as part of running this script
- `{{date}}`: represents the start date of the person being onboarded - you will be prompted to specify this as part of running this script
- `{{epic_key}}`: represents the key of the epic that will be created as a result of running this script. you can use this if you need to link created issues back to this epic.


## custom field support
To support custom fields and JIRA add-ons, you may provide an extension to a custom field (ie. `customfield_12345`) for the following add-ons:

### [Issue Checklist](https://marketplace.atlassian.com/plugins/com.gebsun.plugins.jira.issuechecklist/cloud/overview)
Append `.gebsun_checklist` to the custom field ID key, such as `customfield_12345.gebsun_checklist`, and provide a JSON list of strings as its value to create the checklist. For example:

	"customfield_12345.gebsun_checklist": [
        "Item #1",
        "Item #2",
        "Item #3"
    ]

Also, make sure that "Checklist Content" is an field in Issue Edit.

## example
### (core-eng.json)
	{
	  "server": "https://myserver.atlassian.net",
	  "name": "Core Engineering",
	  "project_key": "PK",
	  "epic_fields": {
		"summary": "Onboarding {{name}} starts {{date}}",
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
		  "assignee": { "name" : "jake" },
		  "customfield_12345.gebsun_checklist": [
			"Make sure dev box is setup for interactive session",
			"Follow up with questions for trainer"
		  ]
		}
	  ]
	}

# dependancies
This is a self contained python script running in a virtualenv wrapped in a bash script.

The bash script downloads [virtualenv](https://virtualenv.pypa.io/en/stable/) and uses pip to install the python jira client inside.

This environment is used to execute a python script making use of the [Python Jira client](https://pythonhosted.org/jira/), so no need to mess with the python install on your machine.

A config file similar to the one above is required to use, and a jira server which you have permission to access must be specified in it.

# Things to do
- Add unit tests
- Config validation against Jira server requirements?
