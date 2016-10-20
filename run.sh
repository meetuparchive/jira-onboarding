#!/bin/bash

DIR="env"
ENV_BASE="jira-env"

VERSION=00.00.03

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
mode="$1"
shift
if [ "$mode" == "exec" ]; then
	$PYTHON src/py/main.py $@
elif [ "$mode" == "webserver" ]; then
	op="$1"
	shift
	pid=$(ps aux | awk '/src\/py\/server.py/ {print $2}') || 0
	if [ "$op" == "start" ]; then
	# is the server running?
		if [[ $pid -eq 0 ]]; then
			nohup $PYTHON src/py/server.py > server.log &
		else
			echo "Server already running!"
		fi
	elif [ "$op" == "stop" ]; then
		if [[ $pid -eq 0 ]]; then
			echo "Server not running!"
		else
			kill -15 $pid
		fi
	elif [ "$op" == "restart" ]; then
		if [[ $pid -ne 0 ]]; then
			kill -15 $pid
		fi
		nohup $PYTHON src/py/server.py > server.log &
	else
		echo "Specify an action to take (start|stop|restart)"
	fi
else
	echo "Please specify mode to run (exec|webserver)"
fi



