'''
PDDL Merge and Translator - Planner Module

Author: Dr. Patricia Riddle @ 2013

Functions for calling an external planner in order to validate and process the intermediary problem files

'''

import os
import sys
import subprocess
from pddl_debug import _DEBUG, _D
from pddl_debug import _PRINT, _P
import pddl_config as conf
from pddl_timeit import timeit


def execute():
    os.system("bash %s/bin/script10-final-optimal %s" % (conf.APP_ROOT, conf.FASTDOWNWARD_ROOT))
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

def runvalidation(new_plan):                                            #! code that ran the validator with the final solution....also not run anymore
    _DEBUG("new_plan_yea",new_plan)
    solutionstring = tostring(new_plan)
    _DEBUG("solutionstring",solutionstring)
    _DEBUG("test",solutionstring[1:-1])
    solution_file = open("sas_plan_new", "w")
    solution_file.write(solutionstring[1:-1])
    solution_file.close()
    test_file = open("tester","w")
    subprocess.call(["%s/src/validate newdomain.pddl newprob.pddl sas_plan" % conf.FASTDOWNWARD_ROOT], shell=True, stdout=test_file)
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

