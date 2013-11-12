#!/bin/bash
#

################################################
#
# PDDL Merge and Translator - Install the PyReform tests
#
# Author: Dr. Patricia Riddle @ 2013
# Contact: pat@cs.auckland.ac.nz
#
# Translates PDDL files using an automated planner in order to improve performance
#
# Installs the PyReform system tests
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

 
