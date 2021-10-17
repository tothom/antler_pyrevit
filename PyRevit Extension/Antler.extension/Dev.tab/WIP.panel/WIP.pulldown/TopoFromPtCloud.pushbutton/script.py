from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms

from collections import OrderedDict
from System.Collections.Generic import List

__doc__ = "Create Toposurface from imported Point Cloud"
__title__ = "Topo from PtCloud"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

def extract_ptcloud_pts(cloud, rectangle, margin=10):
    pass
