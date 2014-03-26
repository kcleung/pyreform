#!/bin/bash
#

################################################
#
# PDDL Merge and Translator - Script to execute the planner
#
# Author: Dr. Patricia Riddle @ 2013
# Contact: pat@cs.auckland.ac.nz
#
# Translates PDDL files using an automated planner in order to improve performance
#
# Planner specific script for executing the planner over reformulated input
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

# Use default locations unless passed in by argument
PYREFORM_HOME="/opt/pddl"
PLANNER_HOME="/opt/planner"

if [ $# > 0 ]
then
	PYREFORM_HOME=$1
	PLANNER_HOME=$2
fi

export PYREFORM_HOME
export PLANNER_HOME

echo $PYREFORM_HOME

export CISSTOPCONT=1


#cd /Users/prid013/Documents/IPCdomains/results-gripper-generated/
count=0
    name="" #`hostname`
    #name=`../code/strip.py $name`
    name+='-'
    name+=$count
    downwardtmp="downwardtmp"$name
    rmdir $downwardtmp
    mkdir $downwardtmp
    echo $downwardtmp
    filename5="downward-test-new-final-1-"$name"infinite-lmcut"
#    output="output"$name
#    outputsas="output.sas"$name
echo "filename" $filename5 > helpme2
    cat $PYREFORM_HOME/bin/planner.sh > $filename5
    date >> $filename5
    cd $downwardtmp
echo $filename5
    nice -n19 python27 $PLANNER_HOME/src/translate/translate.py ../newdomain.pddl ../newprob.pddl >> $filename5
#cat output.sas > $outputsas
    nice -n19 $PLANNER_HOME/src/preprocess/preprocess < output.sas >> $filename5
timename="time"$name
    touch $timename
#cat output > $output
#    echo "outputsas" >> $filename5
#    cat $outputsas >> $filename5
#    echo "output" >> $filename5
#    cat $output >> $filename5
    rm $timename
 echo "lmcut" >> $filename5
 (time $PLANNER_HOME/src/search/\
downward-1 --search "astar(ipdb())" < output >> $filename5) 1> /dev/null 2>> time
#downward-4 --search "astar(blind())" < output >> $filename5) 1> /dev/null 2> time
#downward-4 --search "astar(lmcut())" < output >> $filename5) 1> /dev/null 2> time
    cat time >> $filename5
    #cp sas_plan ..
#    rm time
#    rm $outputsas
#    rm $output
#    rm all.groups
#    rm elapsed.time
#    rm output
#    rm output.sas
#    rm plan_numbers_and_cost
#    rm sas_plan.1
#    rm sas_plan
#    rm test.groups
#    cd ..
#    rmdir $downwardtmp



