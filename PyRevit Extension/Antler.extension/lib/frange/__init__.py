"""
frange
======

Package of functions for plotting.


"""

# init file

import os

_mypackage_root_dir = os.path.dirname(__file__)
_version_file = open(os.path.join(_mypackage_root_dir, 'VERSION'))
__version__ = _version_file.read().strip()

# the following line imports all the functions from frange.py
from .frange import *

