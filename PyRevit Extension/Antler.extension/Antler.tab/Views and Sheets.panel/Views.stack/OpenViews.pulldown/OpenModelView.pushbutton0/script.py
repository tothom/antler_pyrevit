"""
"""
from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms

from collections import OrderedDict
from System.Collections.Generic import List



open_views = revit.uidoc.GetOpenUIViews()

active_docs = {}

# collector = DB.FilteredElementCollector(doc)
# collector.WhereElementIsNotElementType()
# collector.OfClass(DB.View)
#
# views = collector.ToElements()
#
# latest_view = sorted(views, key=lambda x:x.Id.IntegerValue, reverse=True)[0]

uidoc.ActiveView = latest_view
