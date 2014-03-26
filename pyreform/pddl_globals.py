'''
PDDL Merge and Translator - Ancillary Functions

Author: Dr. Patricia Riddle @ 2013
Contact: pat@cs.auckland.ac.nz

Translates PDDL files using an automated planner in order to improve performance

Global Variables used across the application

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

global final_state 
final_state = []

global locations_in_list 
locations_in_list = []

global locations_max 
locations_max = []

global which
which = []

global new_actions
new_actions = []

global DOUBLE_LOOP 
DOUBLE_LOOP = False

global complete_object_list
complete_object_list = []

global  notequalno_type
notequalno_type = []


global unary_params
unary_params = []

global  store_nots
store_nots = []

global goal_name
goal_name = []

global switch
switch = []

global variable_pred_list
variable_pred_list =[]

global current_precond
current_precond = []

global pats_favorite
pats_favorite =[]

global newparam
newparam =[]

global temporary_variables
temporary_variables = []

global bound_variables
bound_variables = []

global temporary_bindings
temporary_bindings = []

global max_num
max_num = 0

global goal_direct
goal_direct = []

global direct_count 
direct_count = 0

global store_big_effects
store_big_effects = []

global big_more
big_more = []

global unary_more
unary_more = []

global goal_more
goal_more = []

global direct
direct = []

global removed_prednames
removed_prednames = []

global store_effects
store_effects = []

global removed_goals
removed_goals = []

global unary_singleton_removal
unary_singleton_removal = []

global notequal
notequal = False

global notequalvar
notequalvar = []

global did_split
did_split = False

global variable_counter
variable_counter = 0

global new_object_list 
new_object_list = []

global unary_big
unary_big = []

global unary_singleton
unary_singleton = []

global unary_goal_preds
unary_goal_preds = []

global additional_actions
additional_actions = []

global all_preds
all_preds = []

global removed_pred
removed_pred = []

global all_lists
all_lists = []

global count_name
count_name="count1a1a"

global count_count
count_count = 0

global num_count
num_count = []

global new_variables
new_variables = []

global extra_nos
extra_nos = []
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

#global new_goals
#new_goals = []

global TYPING
TYPING = False

global new_predicate
new_predicate = []

global thetypes
thetypes = []

global typeof
typeof = None

global more_count
more_count=0

global multiple_reforms
multiple_reforms = False

global second_time
second_time = False

global unary_preds
unary_preds = []

global added_goal
added_goal = False

global unary_new_preds
unary_new_preds = []

global save_unary_predicates
save_unary_predicates = []

global total_save_unary_predicates
total_save_unary_predicates = []

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
