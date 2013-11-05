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
        
        

