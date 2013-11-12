'''
PDDL Merge and Translator - Timing Functions

Author: Dr. Patricia Riddle @ 2013
Contact: pat@cs.auckland.ac.nz

Translates PDDL files using an automated planner in order to improve performance

Utility functions for obtaining performance/timing information

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
import time
import pddl_utils as utils

class timeit(object):

    filename = ""
    markername = ""

    current_file = None
    start_time = 0
    current_time = 0
    marker_increment = 0

    def __init__(self, filename, markername):
        self.filename = filename
        self.markername = markername

    def start(self, *args):
       self.current_file = open(self.filename, "a")
       self.start_time = time.clock()
       if len(args) > 0:
           for arg in args:
               self.current_file.write("%s\n" % arg)
       self.current_time = self.start_time

    def capture(self, *args):
        new_time = time.clock()
        if len(args) > 0:
            self.current_file.write("%s\n" % args[0])
        self.marker_increment += 1
        self.current_file.write("%s_%d: %s\n" % (self.markername, self.marker_increment, str(new_time - self.current_time)))
        self.current_time = new_time
        
    def stop(self, *args):
        stop_time = time.clock()
        if len(args) > 0:
            self.current_file.write("%s\n" % args[0])
        self.current_file.write("total time elapsed: %s\n" % (str(stop_time - self.start_time)))
        self.current_file.close()
        
        

