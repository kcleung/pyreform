'''
PDDL Merge and Translator - Ancillary Functions

Author: Dr. Patricia Riddle @ 2013

Translates PDDL files using an automated planner in order to improve performance

Global Variables used across the application
'''

global storage
storage = []
global storage2
storage2 = []
global storage3
storage3 = []

global NEWPREDICATE
NEWPREDICATE = False
global totalnumber
global ontology
ontology = []
totalnumber = 0
global direction
direction = []

global newfound
newfound = False
global savepredicate

global save_objects
save_objects = []
global new_goals
new_goals = []

global TYPING
TYPING = False

global new_predicate
new_predicate = []
global typeof
typeof = None

global var1
var1 = None
global var2
var2 = None
global predicate
predicate = None

global recurse
recurse = 0

global HASMETRIC
HASMETRIC = False
global metric
metric = None

global HAVEFUNCTIONS
HAVEFUNCTIONS = False
global functions
functions = None

global HASREQUIREMENTS
HASREQUIREMENTS = False
