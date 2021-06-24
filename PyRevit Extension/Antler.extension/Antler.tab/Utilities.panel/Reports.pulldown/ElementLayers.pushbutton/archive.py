# -*- coding: utf-8 -*-

from rpw import revit, DB, UI
from pyrevit import forms, script
import re

lib_path  = re.split('\w*\.extension', __commandpath__)[0] + 'lib'
import sys
if not lib_path in sys.path:
    sys.path.append(lib_path)

import antler

__doc__ = "Get Element Material Layers"
__title__ = "Element Layers"
__author__ = "Thomas Holth"


elements = [revit.doc.GetElement(id) for id in revit.uidoc.Selection.GetElementIds()]

element = elements[0]  # TODO: Modify script for multiple elements.

definition_dict = {
    parameter.Definition.Name: parameter.Definition
    for parameter in element.WallType.Parameters}

selected_definitions = forms.SelectFromList.show(
    sorted(definition_dict.keys()),
    title='Select Parameters',
    multiselect=True
)

# print(selected_definitions)

data = []

wall_type_dict = antler.interop.wall_to_dict(
    element.WallType, include_parameters=selected_definitions)

print(wall_type_dict)

# for f in family_symbols_list:
#     data_row = []
#
#     for key in selected_definitions:
#         data_row.append(f[key])
#
#     data.append(data_row)

output = script.get_output()

output.print_table(
    table_data=[wall_type_dict.keys(), wall_type_dict.values()],
    # title="All Types for Family: {}".format(element.Symbol.Family.Name),
    columns=['Parameter', 'Value']
)
