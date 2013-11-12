#!/bin/bash
#

################################################
#
# PDDL Merge and Translator - Executes a sequence of regression calls
#
# Author: Dr. Patricia Riddle @ 2013
# Contact: pat@cs.auckland.ac.nz
#
# Translates PDDL files using an automated planner in order to improve performance
#
# Program: to run a sequence of regression tests over the PDDL Translator program
#	      produces a PASS or FAIL based on similarity with a provided output file
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


PYREFORM_HOME=`echo $0 | awk -F "/bin/" '{ print $1 }'`
export PYREFORM_HOME

#gripper
$PYREFORM_HOME/bin/single_test.sh gripper prob01.pddl
$PYREFORM_HOME/bin/single_test.sh gripper prob02.pddl
$PYREFORM_HOME/bin/single_test.sh gripper prob03.pddl
$PYREFORM_HOME/bin/single_test.sh gripper prob04.pddl
$PYREFORM_HOME/bin/single_test.sh gripper prob05.pddl

#nomystery-opt11
$PYREFORM_HOME/bin/single_test.sh nomystery-opt11 p01.pddl
$PYREFORM_HOME/bin/single_test.sh nomystery-opt11 p02.pddl
$PYREFORM_HOME/bin/single_test.sh nomystery-opt11 p03.pddl
#$PYREFORM_HOME/bin/single_test.sh nomystery-opt11 p04.pddl
$PYREFORM_HOME/bin/single_test.sh nomystery-opt11 p05.pddl 

#transport1
$PYREFORM_HOME/bin/single_test.sh transport-opt11-strips p01.pddl
$PYREFORM_HOME/bin/single_test.sh transport-opt11-strips p02.pddl
$PYREFORM_HOME/bin/single_test.sh transport-opt11-strips p03.pddl
$PYREFORM_HOME/bin/single_test.sh transport-opt11-strips p04.pddl
$PYREFORM_HOME/bin/single_test.sh transport-opt11-strips p05.pddl 
