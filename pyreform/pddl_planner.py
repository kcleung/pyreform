'''
PDDL Merge and Translator - Planner Module

Author: Dr. Patricia Riddle @ 2013
Contact: pat@cs.auckland.ac.nz

Functions for calling an external planner in order to validate and process the intermediary problem files

-------

Copyright (C) 2013  Dr. Patricia Riddle, University of Auckland

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

import os
import sys
import subprocess
from pddl_debug import _DEBUG, _D
from pddl_debug import _PRINT, _P
import pddl_config as default_config
from pddl_timeit import timeit


def execute(local_config=None):

    config = default_config
    if not local_config is None:
        config = local_config
        
    os.system("bash %s/bin/planner.sh %s %s" % (config.APP_HOME, config.APP_HOME, config.PLANNER_HOME))
    myfileplan = open("downwardtmp-0/sas_plan")                
    plan = myfileplan.read()
    myfileplan.close()
    return plan

def giveup(domain,prob, domain_file, problem_file):
    _DEBUG("OH NO")
    new_file_name = "newdomain.pddl"
    text_file = open(new_file_name, "w")                                                                #!write prob string into a file
    text_file.write(domain)
    text_file.close()
    new_file_name = "newprob.pddl"
    text_file = open(new_file_name, "w")                                                                #!write prob string into a file
    text_file.write(prob)
    text_file.close()
    timer = timeit("timing.txt", "elapsed")
    timer.start(domain_file, problem_file)
    timer.capture()
    plan = execute()
    timer.capture()
    solution_file = open("sas_plan_new", "w")
    solution_file.write(plan)
    solution_file.close()
    timer.capture()
    timer.stop()
    return []

def runvalidation(new_plan, local_config=None):                                            #! code that ran the validator with the final solution....also not run anymore

    config = default_config
    if not local_config is None:
        config = local_config

    _DEBUG("new_plan_yea",new_plan)
    solutionstring = tostring(new_plan)
    _DEBUG("solutionstring",solutionstring)
    _DEBUG("test",solutionstring[1:-1])
    solution_file = open("sas_plan_new", "w")
    solution_file.write(solutionstring[1:-1])
    solution_file.close()
    test_file = open("tester","w")
    subprocess.call(["%s/src/validate newdomain.pddl newprob.pddl sas_plan" % config.PLANNER_HOME], shell=True, stdout=test_file)
    _DEBUG("subprocess",subprocess) 
#!    omp_cmd = '/Users/prid013/Documents/Fast-Downward-8ea549f76262/src/validate /Users/prid013/Documents/IPCdomains/benchmarks3/gripper/domain.pddl /Users/prid013/Documents/IPCdomains/benchmarks3/gripper/prob01.pddl /Users/prid013/Documents/IPCdomains/sas_plan_new' 
#!with open(test_file) as stdout:
#!    xmlResult = Popen(shlex.split(omp_cmd), stdin=stdin, stdout=PIPE, stderr=STDOUT)
    test_file.close()
    test_file = open("tester","r")
    output = test_file.read()
    _DEBUG("output",output)
    if "Successful" in output:
        return new_plan
    else:
        return False

