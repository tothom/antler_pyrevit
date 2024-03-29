"""
"""
from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms

from collections import OrderedDict
from System.Collections.Generic import List

uidoc = revit.uidoc
doc = revit.doc
app = revit.app

element_ids = List[DB.ElementId]()

collector = DB.FilteredElementCollector(doc, uidoc.ActiveView.Id)
elements = collector.ToElements()

element_ids.AddRange([e.Id for e in elements])

uidoc.Selection.SetElementIds(element_ids)
