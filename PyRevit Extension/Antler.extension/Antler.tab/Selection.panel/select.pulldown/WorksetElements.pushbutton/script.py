from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms

from collections import OrderedDict
from System.Collections.Generic import List

__doc__ = "Gets all Elements in Workset"
__title__ = "Elements in Workset"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

def get_elements_on_workset(workset):
    """
    """
    element_collector = DB.FilteredElementCollector(doc)
    element_workset_filter = DB.ElementWorksetFilter(workset.Id)
    workset_elements = element_collector.WherePasses(element_workset_filter).ToElements()

    return workset_elements

# Select Levels
fwc = DB.FilteredWorksetCollector(doc)
fwc.OfKind(DB.WorksetKind.UserWorkset).ToWorksets()

workset_dict = {"{}".format(w.Name): w for w in fwc}

workset_dict = OrderedDict(sorted(workset_dict.items(), key=lambda (key, value): value.Name))
workset_key = forms.SelectFromList.show(workset_dict.keys(), button_name='Select Workset', multiple=False, message='Select Workset to collect Elements.')
workset = workset_dict.get(workset_key) # Using get() to avoid error message when cancelling dialog.
# worksets = forms.select_worksets()

elements = []

if workset:
    # for workset in worksets:
    elements.extend(get_elements_on_workset(workset))

element_id_collection = List[DB.ElementId]([element.Id for element in elements])

uidoc.Selection.SetElementIds(element_id_collection)
