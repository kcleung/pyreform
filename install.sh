#!/bin/bash
#

################################################
#
# PDDL Merge and Translator - Install the PyReform system
#
# Author: Dr. Patricia Riddle @ 2013
# Contact: pat@cs.auckland.ac.nz
# Version: 2.0
#
# Translates PDDL files using an automated planner in order to improve performance
#
# Installs the PyReform system
#
# -------
#
# Copyright (C) 2013  Dr. Patricia Riddle, University of Auckland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
################################################

PYREFORM_REPOSITORY="https://pyreform.googlecode.com/svn/trunk"
export PYREFORM_REPOSITORY

PYREFORM_HOME="/opt/pddl"
PLANNER_HOME="/opt/planner"

ANS="N"
read -p "This script will install the PyReform system. Do you wish to continue? [y/N] " ANS
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

read -p "Enter planner home directory [$PLANNER_HOME]: " ANS

if [ "$ANS" != "" ]
then
        PLANNER_HOME=$ANS
fi

export PYREFORM_HOME
export PLANNER_HOME

echo "Setting up key directories..."
echo

# If PYREFORM_HOME exists but is not a directory then exit
if [ -f $PYREFORM_HOME ]
then
	echo "Your PyReform home path is not a directory! Exiting now..."
	exit
fi

# If PYREFORM_HOME does not exist as a directory then create it
if [ ! -d $PYREFORM_HOME ]
then
	mkdir $PYREFORM_HOME
	echo "$PYREFORM_HOME..."
fi

# If PYREFORM_HOME/bin does not exist then create it but exit if it does exist
if [ ! -d "$PYREFORM_HOME/bin" ]
then
	mkdir "$PYREFORM_HOME/bin"
	echo "$PYREFORM_HOME/bin..."
else
	echo "Your PyReform home path is not empty! Exiting now..."
	exit
fi

# Install the system license
echo  
echo "Installing the license file..."
echo

wget --no-check-certificate $PYREFORM_REPOSITORY/LICENSE.txt
cp LICENSE.txt $PYREFORM_HOME

# Start installing PyReform itself
echo "Installing the core PyReform modules..."
echo 

# Determine how to install the core PyReform modules
ANS="local"
read -p "install locally or as Python modules? [local/python] " ANS

BASE_INSTALL_TYPE=$ANS
export BASE_INSTALL_TYPE

# install the core PyReform modules according to type
if [ "$BASE_INSTALL_TYPE" == "local" ]
then
	svn export $PYREFORM_REPOSITORY/pyreform
	mkdir $PYREFORM_HOME/bin/pyreform
	cd pyreform
	cp *.py $PYREFORM_HOME/bin/pyreform
	cd ..
else
	easy_install "$PYREFORM_REPOSITORY#egg=pyreform"
fi

echo
echo "Installing the PyReform scripts..."
echo

# install the main PyReform scripts
svn export $PYREFORM_REPOSITORY/bin
cd bin
cp *.* $PYREFORM_HOME/bin
cd ..
chmod a+rx $PYREFORM_HOME/bin/*.sh

echo "Updating the PyReform configuration..."
echo

echo "APP_HOME = '$PYREFORM_HOME'" > $PYREFORM_HOME/bin/config.py
echo "PLANNER_HOME = '$PLANNER_HOME'" >> $PYREFORM_HOME/bin/config.py

echo "Installing the default planner..."
echo

if [ -f $PLANNER_HOME ]
then
	echo "$PLANNER_HOME is not a directory. Exiting now..."
	exit
fi

# If the PLANNER_HOME does not exist then create the directory and install the planner
if [ ! -d $PLANNER_HOME ]
then	
	mkdir $PLANNER_HOME
	
	# install the planner files
	wget --no-check-certificate $PYREFORM_REPOSITORY/planners/fastdownward/fastdownward-latest.tgz
	CURDIR=`pwd`
	cd $PLANNER_HOME
	tar xzvf $CURDIR/fastdownward-latest.tgz	

	# build the planner programs
	cd src
	./build_all
	
	cd $CURDIR	
	
	# install the planner script
	wget --no-check-certificate $PYREFORM_REPOSITORY/planners/fastdownward/planner.sh
	cp planner.sh $PYREFORM_HOME/bin
	chmod a+rx $PYREFORM_HOME/bin/planner.sh
fi

# Check if the user wishes to install the tests and if so install them
INSTALL_TESTS="N"
read -p "Do you want to install the PDDL problem test files? [y/N] " INSTALL_TESTS

if [ "$INSTALL_TESTS" == "y" ]
then
	echo "Installing the PDDL problem tests..."
	echo
	
	svn export $PYREFORM_REPOSITORY/tests
	mkdir $PYREFORM_HOME/tests
	cd tests
	cp -r * $PYREFORM_HOME/tests
	cp bin/*.sh $PYREFORM_HOME/bin	
	cd ..
	chmod a+rx $PYREFORM_HOME/bin/*.sh
fi

echo "Done!"

 
