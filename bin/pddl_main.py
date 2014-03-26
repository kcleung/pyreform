'''
PDDL Merge and Translator - Entry point script

Author: Dr. Patricia Riddle @ 2013
Contact: pat@cs.auckland.ac.nz
Version: 2.0

Translates PDDL files using an automated planner in order to improve performance

Script to run to start use of system

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

import sys
import pyreform.pddl_merge as main
import config

result = main.run(sys.argv[1], sys.argv[2], sys.argv[3], local_config=config) # pats comment to prove she can commit

