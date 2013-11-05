# Copyright (C) 2013  Patricia Riddle <pat@cs.auckland.ac.nz>
#
# This file is part of PyReform
#
# 'PyReform' is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 3.0 of the License, or (at your option)
# any later version.
#
# 'PyReform' is distrubuted in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with 'ssh'; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Suite 500, Boston, MA  02110-1335  USA.


longdesc = '''
This is a set of programs for reformulating PDDL files ready for input into automated planners.
'''

import ez_setup
ez_setup.use_setuptools()

import sys
try:
    from setuptools import setup
    kw = {
        #'install_requires': 'pycrypto >= 2.1, != 2.4',
    }
except ImportError:
    from distutils.core import setup
    kw = {}

setup(name = "pyreform",
      version = "1.9.0",
      description = "PyReform PDDL reformulator",
      author = "Patricia Riddle",
      author_email = "pat@cs.auckland.ac.nz",
      url="https://pyreform.googlecode.com/svn/trunk",
      packages = [ 'pyreform' ],
      license = 'LGPL',
      platforms = 'Posix; MacOS X; Windows',
      classifiers = [ 'Development Status :: 3 - Development',
                      'Intended Audience :: Researchers',
                      'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                      'Operating System :: OS Independent',
                      'Topic :: AI',
                      'Topic :: Reformulation :: Python' ],
      long_description = longdesc,
      **kw
      )
