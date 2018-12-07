#!/bin/sh

if [ ! -f "app/runserver.py" ]
then
	echo "app/runserver.py is not there."
fi

exec python3 runserver.py

