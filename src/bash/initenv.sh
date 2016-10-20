#!/bin/bash

###
# This is a script for fetching and installing the jira client
# within a virtualenv, and should be environment-dependancy free.
# We download the virtualenv distribution, create an environment
# and install the jira client within that environment
###

### SETUP ###
# virtualenv version
VIRTUALENV_VERSION=15.0.1

# other libs versions
PYYAML_VERSION=3.12
KLEIN_VERSION=15.3.1

# use current python
PYTHON=$(which python)

# where to d/l virtualenv
URL_BASE=https://pypi.python.org/packages/source/v/virtualenv

# virtualenv directory to live in
if [ -z "$1" ]; then
	echo "USAGE: initenv.sh [ENV] [VERSION]"
	echo "Must provide name of directory (to be created) where client environment will live"
	exit
fi
INITIAL_ENV=$1

# transifex client version to use
if [ -z "$2" ]; then
	echo "USAGE: initenv.sh [ENV] [VERSION]"
	echo "Must provide the version of the jira client to use"
	exit
fi
JIRA_CLIENT_VERSION=$2

# If directory already exists, assume its already set up
if [ -d "$INITIAL_ENV" ]; then
	echo "Directory $INITIAL_ENV already exists!"
	echo "To re-set-up, delete this directory and then rerun this script"
	exit
fi

echo "***Setting up jira client! Hold tight***"
echo "***Using virtualenv version $VIRTUALENV_VERSION***"
echo
### do work ###
# get virtualenv dist, and extract
echo
echo "***Downloading virtualenv***"
curl -O $URL_BASE/virtualenv-$VIRTUALENV_VERSION.tar.gz
echo
echo "***Extracting virtualenv***"
tar xzf virtualenv-$VIRTUALENV_VERSION.tar.gz

# create environment
echo
echo "***creating new virtualenv in $INITIAL_ENV***"
$PYTHON virtualenv-$VIRTUALENV_VERSION/virtualenv.py $INITIAL_ENV

# Don't need this anymore.
echo
echo "Cleaning up downloaded files"
rm -rf virtualenv-$VIRTUALENV_VERSION
rm -rf virtualenv-$VIRTUALENV_VERSION.tar.gz

# install transifex client into environment
echo
echo "***Installing jira client in $INITIAL_ENV***"
$INITIAL_ENV/bin/pip install jira==${JIRA_CLIENT_VERSION}

echo "***Installing pyyaml in $INITIAL_ENV***"
$INITIAL_ENV/bin/pip install PyYAML==${PYYAML_VERSION}

echo "***Installing klein in $INITIAL_ENV***"
$INITIAL_ENV/bin/pip install klein==${KLEIN_VERSION}

echo
echo ***Done setting up jira client***
echo
