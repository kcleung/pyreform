#!/bin/bash
#

PYREFORM_REPOSITORY="https://pyreform.googlecode.com/svn/trunk"
export PYREFORM_REPOSITORY

PYREFORM_HOME="/opt/pddl"

ANS="N"
read -p "This script will install the PyReform tests. Do you wish to continue? [y/N] " ANS
if [ "$ANS" != "y" ]
then
	exit
fi

echo "Gathering key directory paths..."
echo

read -p "Enter PyReform home directory [$PYREFORM_HOME]: " ANS

if [ "$ANS" != "" ]
then
	PYREFORM_HOME=$ANS
fi

export PYREFORM_HOME

echo "Installing the PDDL problem tests..."
echo
	
svn export $PYREFORM_REPOSITORY/tests
mkdir $PYREFORM_HOME/tests
cd tests
cp -r * $PYREFORM_HOME/tests
cp bin/*.sh $PYREFORM_HOME/bin	
cd ..
chmod a+rx $PYREFORM_HOME/bin/*.sh

echo "Done!"

 
