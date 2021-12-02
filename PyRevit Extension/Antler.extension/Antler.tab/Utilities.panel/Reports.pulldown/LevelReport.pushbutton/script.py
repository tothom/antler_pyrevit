from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script

from collections import OrderedDict
from System.Collections.Generic import List

import antler.util

logger = script.get_logger()
output = script.get_output()


# Select Levels

levels = DB.FilteredElementCollector(revit.doc).OfCategory(
    DB.BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()


data = []

# counts = []

for level in levels:
    level_filter = DB.ElementLevelFilter(level.Id)
    collector = DB.FilteredElementCollector(revit.doc)
    collector.WherePasses(level_filter)#.ToElements()

    count = collector.GetElementCount()

    data.append({
        'Level Name': level.Name,
        'Element Count': count
    })

    # counts.append(counts)

    # print("{}: {}".format(level.Name, count))

def print_dict_list_as_table(data, title="", formats=[]):
    keys = set().union(*(d.keys() for d in data))

    if not formats:
        formats = ['' for _ in keys]

    output.print_table(
        table_data=[[a.get(k) for k in keys] for a in data],
        title=title,
        columns=keys,
        formats=formats
    )

antler.util.print_dict_list_as_table(data, title="Level Element Count")

# keys = set().union(*(d.keys() for d in data))
#
# # data = [[a.get(key) for a in level_data] for key in keys]
#
# logger.debug(data)
#
# output.print_table(
#     table_data=[[a.get(k) for k in keys] for a in data],
#     title="Level Element Count",
#     columns=keys,
#     formats=['', '']
# )
