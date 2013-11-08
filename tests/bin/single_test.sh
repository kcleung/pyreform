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

PYREFORM_HOME=`echo $0 | awk -F "/bin/" '{ print $1 }'`
export PYREFORM_HOME

export PROGNAME="pddl_main"

python $PYREFORM_HOME/bin/$PROGNAME.py $PYREFORM_HOME/tests/$1/$2/input/domain.pddl $PYREFORM_HOME/tests/$1/$2/input/$2 > prog.out 2> prog.err

DIFF_SIZE=`diff sas_plan_new /opt/pddl2/tests/$1/$2/output/sas_plan_new | wc -c`
if [[ $DIFF_SIZE == '0' ]] 
then
	echo $1":    "$2 ": PASS"
else
	echo $1":    "$2 ": FAIL:"
	diff sas_plan_new $PYREFORM_HOME/tests/$1/$2/output/sas_plan_new
	echo
fi


