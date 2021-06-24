"""
"""
from rpw import revit, DB, UI

# from pyrevit import forms

# from collections import OrderedDict
from System.Collections.Generic import List

__doc__ = "Get host of selected Elements."
__title__ = "Host Element"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc
app = revit.app


current_selection = uidoc.Selection.GetElementIds()

#print(current_selection)

element_ids = List[DB.ElementId]()

for element_id in current_selection:

    element = doc.GetElement(element_id)
    host_element = element.Host

    element_ids.Add(host_element.Id)

uidoc.Selection.SetElementIds(element_ids)
