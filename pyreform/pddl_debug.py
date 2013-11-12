'''
PDDL Merge and Translator - Debug Module

Author: Dr. Patricia Riddle @ 2013
Contact: pat@cs.auckland.ac.nz

Debug and Print functions/macros

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

DEBUG = False

def _DEBUG(*args):

    if DEBUG: print str(args)[1:-1]

_D = _DEBUG


DOPRINT = True

def _PRINT(*args):

    if DOPRINT: print str(args)[1:-1]

_P = _PRINT
