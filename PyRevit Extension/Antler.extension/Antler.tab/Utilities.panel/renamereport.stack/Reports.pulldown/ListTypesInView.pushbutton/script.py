# -*- coding: utf-8 -*-

from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS
import re

# lib_path  = re.split('\w*\.extension', __commandpath__)[0] + 'lib'
# import sys
# if not lib_path in sys.path:
#     sys.path.append(lib_path)

import antler

output = script.get_output()

category = antler.forms.select_category(multiselect=False)

collector = DB.FilteredElementCollector(revit.doc, revit.uidoc.ActiveView.Id)
# collector.WhereElementIsElementType()
collector.OfCategory(antler.util.builtin_category_from_category(category))

elements = collector.ToElements()

output = script.get_output()

names = {}

for element in elements:
    # parameter = element.get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME)
    # print(parameter.AsString)
    if element.Name not in names:
        # print(element.Name)
        names[element.Name] = {'Count': 1, 'Elements': [element]}
    else:
        names[element.Name]['Count'] += 1
        names[element.Name]['Elements'].append(element)

for k, v in names.items():
    

output.print_table(
    title="Types in View",
    table_data=[(k, names[k]['Elements'], names[k]['Count']) for k in names.keys()]
)

# antler.util.print_dict_as_table(names, sort=True, columns=("Type", "Count"))



    # output.print_table(
    #     table_data=data,
    #     title="All Types for Family: {}".format(element.Symbol.Family.Name),
    #     columns=selected_definitions
    # )
    #
    # output.print_md("*Only Type Parameters are shown...*")
