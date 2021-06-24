"""
"""
from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms

from collections import OrderedDict
from System.Collections.Generic import List

__doc__ = "Select all Elements visible in View"
__title__ = "Open Primary View"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc
app = revit.app

primary_view_id = uidoc.ActiveView.GetPrimaryViewId()
primary_view = doc.GetElement(primary_view_id)

if primary_view:
    uidoc.ActiveView = primary_view
else:
    forms.alert("No primary view found. Maybe the view is not dependent?")
