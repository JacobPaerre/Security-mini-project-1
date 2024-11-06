#!/usr/bin/env bash

if [ "$1" = "start" ]; then
	echo "Starting server..."
	nohup python3 app.py > /tmp/out.log 2>&1 &
elif [ "$1" = "stop" ]; then
	echo "Stopping server..."
	pkill -f python3
fi
