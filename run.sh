#!/bin/bash

DIR="env"
ENV_BASE="jira-env"

VERSION=00.00.02

JIRA_CLIENT_VERSION=1.0.7

VERSIONED_ENV="$ENV_BASE-$VERSION"

# if python environment not set up, set it up
if [ ! -d "$DIR" ]; then
	mkdir $DIR
fi;
if [ ! -d "$DIR/$VERSIONED_ENV" ]; then
	pushd $DIR > /dev/null
	../src/bash/initenv.sh $VERSIONED_ENV $JIRA_CLIENT_VERSION
	popd > /dev/null
fi;

PYTHON=$DIR/$VERSIONED_ENV/bin/python
$PYTHON src/py/main.py $@
