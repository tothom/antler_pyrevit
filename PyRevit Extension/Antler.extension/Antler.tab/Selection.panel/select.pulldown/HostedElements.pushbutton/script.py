"""
Source: https://thebuildingcoder.typepad.com/blog/2009/01/filter-for-hosted-elements.html
"""


from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms

from collections import OrderedDict
from System.Collections.Generic import List

__doc__ = "Gets all Elements hosted by selected Elements"
__title__ = "Hosted Elements"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc
app = revit.app

def get_hosted_elements(host):
    """
    """
    provider = DB.ParameterValueProvider(DB.ElementId(DB.BuiltInParameter.HOST_ID_PARAM))
    rule = DB.FilterElementIdRule(provider, DB.FilterNumericEquals(), host.Id)
    parameter_filter = DB.ElementParameterFilter(rule)

    collector = DB.FilteredElementCollector(doc)
    collector.OfClass(DB.FamilyInstance)
    collector.WherePasses(parameter_filter)

    elements = collector.ToElements()

    return elements


current_selection = uidoc.Selection.GetElementIds()

#print(current_selection)

element_ids = List[DB.ElementId]()

for element_id in current_selection:

    host_element = doc.GetElement(element_id)
    hosted_elements = get_hosted_elements(host_element)

    element_ids.AddRange([e.Id for e in hosted_elements])

uidoc.Selection.SetElementIds(element_ids)
