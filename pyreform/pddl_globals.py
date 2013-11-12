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
