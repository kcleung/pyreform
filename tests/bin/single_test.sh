#!/bin/bash
#

# Author: Andrew Probert 2013
# Program: to run a single regression test over the PDDL Translator program
#	      takes as input the name of the test to run
#	      produces a PASS or FAIL based on similarity with a provided output file
#
#	      set PROGNAME to the correct name of the translator program
#
#

ulimit -s 100000
ulimit -v 1500000

export PROGNAME="merge-new"

python /opt/pddl/bin/$PROGNAME.py /opt/pddl/tests/$1/$2/input/domain.pddl /opt/pddl/tests/$1/$2/input/$2 > prog.out 2> prog.err

DIFF_SIZE=`diff sas_plan_new /opt/pddl/tests/$1/$2/output/sas_plan_new | wc -c`
if [[ $DIFF_SIZE == '0' ]] 
then
	echo $1":    "$2 ": PASS"
else
	echo $1":    "$2 ": FAIL:"
	diff sas_plan_new /opt/pddl/tests/$1/$2/output/sas_plan_new
	echo
fi


