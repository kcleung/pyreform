#!/bin/bash
#

PYREFORM_HOME="/opt/pddl"
PLANNER_HOME="/opt/planner"

read -p "Enter directory [$PYREFORM_HOME]: " ANS

if [ "$ANS" != "" ]
then
	PYREFORM_HOME=$ANS
fi

read -p "Enter directory [$PLANNER_HOME]: " ANS

if [ "$ANS" != "" ]
then
        PLANNER_HOME=$ANS
fi

export PYREFORM_HOME
export PLANNER_HOME

if [ ! -d $PYREFORM_HOME ]
then
	mkdir $PYREFORM_HOME
fi

if [ ! -d "$PYREFORM_HOME/bin" ]
then
	mkdir "$PYREFORM_HOME/bin"
fi

echo "Done!"

 
