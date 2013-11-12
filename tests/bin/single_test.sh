#!/bin/bash
#

################################################
#
# PDDL Merge and Translator - Executes a single regression call
#
# Author: Dr. Patricia Riddle @ 2013
# Contact: pat@cs.auckland.ac.nz
#
# Translates PDDL files using an automated planner in order to improve performance
#
# Program: to run a single regression test over the PDDL Translator program
#	      takes as input the name of the test to run
#	      produces a PASS or FAIL based on similarity with a provided output file
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

export PROGNAME="pddl_main"

python $PYREFORM_HOME/bin/$PROGNAME.py $PYREFORM_HOME/tests/$1/$2/input/domain.pddl $PYREFORM_HOME/tests/$1/$2/input/$2 > prog.out 2> prog.err

DIFF_SIZE=`diff sas_plan_new $PYREFORM_HOME/tests/$1/$2/output/sas_plan_new | wc -c`
if [[ $DIFF_SIZE == '0' ]] 
then
	echo $1":    "$2 ": PASS"
else
	echo $1":    "$2 ": FAIL:"
	diff sas_plan_new $PYREFORM_HOME/tests/$1/$2/output/sas_plan_new
	echo
fi


