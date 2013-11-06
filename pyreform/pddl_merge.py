'''
PDDL Merge and Translator - Main Module

Author: Dr. Patricia Riddle @ 2013

Translates PDDL files using an automated planner in order to improve performance

Expects two input files in PDDL format
- one for the domain and one explicitly describing the problem
'''

import copy
import shlex
import re
import sys
#import traceback
from pyparsing import nestedExpr

import pddl_globals as G
from pddl_debug import _DEBUG, _D
from pddl_debug import _PRINT, _P
import pddl_reformulation as reform
import pddl_planner as planner
import pddl_core as core
from pddl_timeit import timeit

sys.setrecursionlimit(10000000)

#%%add newprob and newdomain to each output folder

#%%then do transport - misses truck-02 on the 0 counts....fix ;s
#no-mystery prob02 and prob05 not putting goals in (have not tried 6 on) - fixed!! - but no-mystery has lots of problems....skipping for now
#nomystery-sat11 prob2 and p12 dies on solution string (have not tried 13 on) - fixed! - must test
#%%elevators 2008   dies on p07?????



def run(domain_file, problem_file, local_config=None):
    '''
    This is the entry point for the PDDL Reform application
    It expects two input files in PDDL format and generates a set of files in response including:

     - reformulated input files
     - a regenerated sas plan file
    '''    

    if not local_config is None:
        names = dir(local_config)
        if not 'APP_ROOT' in names and not 'FASTDOWNWARD_ROOT' in names:
            local_config = None

    # Read in the domain and problem input files
    domain, prob = core.read_input(domain_file, problem_file)

    G.HASMETRIC = False
    G.HAVEFUNCTIONS = False
    G.HASREQUIREMENTS = False

    # Parse the domain input
    domain2, requirements, predicates, types, actions, domain_list1_real, domain_list1_temp = core.parse_domain(domain)

    # Form a deep copy of the actions component
    _DEBUG("requirements",requirements)
    _DEBUG("actions",actions)
    old_actions = copy.deepcopy(actions)                                       #! do not remember why I had to do this
    _DEBUG("helphelp",old_actions)

    # Parse the problem input
    prob2, objects1, goals, init, prob_list2_real, prob_list2_temp = core.parse_problem(prob)
    
    _DEBUG("objects", objects1)
    _DEBUG("goals", goals)

    # Process the typing if applicable
    ontology, typing, objects, typeof_l, SOKOBAN = core.process_typing(requirements, types, objects1)
    G.typeof = typeof_l
    _PRINT("typeof!", G.typeof)

    # Check whether we can reformulate this input
    REFORMULATE, myset, FOUND = core.test_reformulate(objects, actions, goals, prob2)

    # If we can't reformulate then simply output what was input and exit
    if myset == []:
        #_PRINT("reformulate",REFORMULATE,"myset",myset) #"mylist",mylist
        planner.giveup(domain,prob, domain_file, problem_file)
        sys.exit()
    
    _DEBUG("reformulate", REFORMULATE)

    # Otherwise if we can reformulate the input do so
    if REFORMULATE:                                                                             
        lists = core.reformulate(myset, domain2, requirements, predicates, types, actions, domain_list1_real, domain_list1_temp, prob2, objects1, goals, init, prob_list2_real, prob_list2_temp, ontology, typing, objects, SOKOBAN)
        
    #fix double list first - change gripper to make 2 lists
    #! run lmcut
    #! replace methodologyical

    # Execute the embedded planner over the reformulated input files
    timer = timeit("timing.txt", "elapsed")
    timer.start(domain_file, problem_file)
    timer.capture()
    plan = planner.execute(local_config=local_config)
    timer.capture()
    
    #_PRINT("plan",plan)

    # Post process the resulting sas_plan file
    solution = core.postprocess_plan(plan, lists, init, old_actions)

    _DEBUG("solutionwww",solution)
    #_PRINT("solution", solution)

    # Finally write out the resulting new sas_plan file
    core.writeout_solution(solution)

    _DEBUG("test")
    _DEBUG(reform.fun('D',['ontable','D']) )
    _DEBUG("found", FOUND)

    timer.capture()
    timer.stop()
    
    # And we are done!


if __name__ == '__main__':

    result = run(sys.argv[1], sys.argv[2])
    
