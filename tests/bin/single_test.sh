#!/bin/bash
#

################################################
#
# PDDL Merge and Translator - Executes a single regression call
#
# Author: Dr. Patricia Riddle @ 2013
# Contact: pat@cs.auckland.ac.nz
# Version: 2.0
#
# Translates PDDL files using an automated planner in order to improve performance
#
# Program: to run a single regression test over the PDDL Translator program
#	      takes as input a domain, the name of the test to run and a direction (one of forward or backward)
#	      produces a validation report
#
#	      set PROGNAME to the correct name of the translator program
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

ulimit -s 100000
ulimit -v 1500000

PYREFORM_HOME=`echo $0 | awk -F "/bin/" '{ print $1 }'`
export PYREFORM_HOME

if [[ "$PLANNER_HOME" == "" ]]
then
	PLANNER_HOME="/opt/planner"
	export PLANNER_HOME
fi

export PROGNAME="pddl_main"

TEMP_DIR="pyreform_tmp"
export TEMP_DIR

if [[ -d $TEMP_DIR ]]
then
	echo "$TEMP_DIR already exists! Please delete this directory and run this script again."
	exit 1
fi

mkdir $TEMP_DIR
cd $TEMP_DIR

python $PYREFORM_HOME/bin/$PROGNAME.py $PYREFORM_HOME/tests/$1/$2/input/domain.pddl $PYREFORM_HOME/tests/$1/$2/input/$2 "$3"> /dev/null 2> prog.err

#DIFF_SIZE=`diff sas_plan_new $PYREFORM_HOME/tests/$1/$2/output/sas_plan_new | wc -c`

echo
echo "Validating "$1":    "$2
$PLANNER_HOME/src/validate $PYREFORM_HOME/tests/$1/$2/input/domain.pddl $PYREFORM_HOME/tests/$1/$2/input/$2 sas_plan_new | $PYREFORM_HOME/bin/strip.py

rm -r *
cd ..
rmdir $TEMP_DIR
