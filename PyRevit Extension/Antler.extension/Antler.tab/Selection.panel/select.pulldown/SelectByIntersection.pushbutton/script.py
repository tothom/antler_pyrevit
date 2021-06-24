from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms

from collections import OrderedDict
from System.Collections.Generic import List

__doc__ = "Select Elements intersecting with selected Element"
__title__ = "Select By Intersection"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

# Select Levels
current_selection = uidoc.Selection.GetElementIds()

elements = []

for selection_id in current_selection:
    selection = doc.GetElement(selection_id)
    intersection_filter = DB.ElementIntersectsElementFilter(selection)

    filtered_element_collector = DB.FilteredElementCollector(doc, revit.active_view.Id)

    collected_elements = filtered_element_collector.WherePasses(intersection_filter).ToElements()

    elements.extend(collected_elements)

element_id_collection = List[DB.ElementId]([element.Id for element in elements])

uidoc.Selection.SetElementIds(element_id_collection)
