#!/bin/bash
#

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
