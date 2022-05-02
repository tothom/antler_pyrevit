from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import script
from collections import OrderedDict

__doc__ = "Creates a report of Worksets in model."
__title__ = "Worksets Report"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

# worksets = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Worksets).WhereElementIsNotElementType().ToElements()
worksets = DB.FilteredWorksetCollector(doc).OfKind(DB.WorksetKind.UserWorkset)

worksets_dict = {}

for workset in worksets:
    workset_filter = DB.ElementWorksetFilter(workset.Id)
    collector = DB.FilteredElementCollector(doc).WherePasses(workset_filter).WhereElementIsNotElementType()

    worksets_dict[workset.Name] = collector.GetElementCount()

worksets_dict = OrderedDict(sorted(worksets_dict.items())) # Sort worksetlist

output = script.get_output()

output.print_table(
    table_data=worksets_dict.items(),
    title="Workset Element Count",
    columns=["Workset", "Count"],
    formats=['', '']
)

# Write log
import os
log_path = os.path.join(__commandpath__, 'worksets.log')

with open(log_path, 'w') as f:
    [f.write("{}: {}\r\n".format(key, value)) for key, value in worksets_dict.items()]
