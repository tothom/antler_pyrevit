# -*- coding: utf-8 -*-

from rpw import revit, DB, UI
from pyrevit import forms, script
import re

# lib_path  = re.split('\w*\.extension', __commandpath__)[0] + 'lib'
# import sys
# if not lib_path in sys.path:
#     sys.path.append(lib_path)

import antler

__doc__ = "List all Types of a Family"
__title__ = "List Types"
__author__ = "Thomas Holth"


elements = [revit.doc.GetElement(id) for id in revit.uidoc.Selection.GetElementIds()]
element = elements[0]  # TODO: Modify script for multiple elements.

selected_definitions = antler.ui.select_element_parameters(element.Symbol)

data = []

family_symbols_list = antler.interop.family_to_dict(
    element.Symbol.Family, include_parameters=selected_definitions)

for f in family_symbols_list:
    data_row = []

    for key in selected_definitions:
        data_row.append(f[key])

    data.append(data_row)

output = script.get_output()

output.print_table(
    table_data=data,
    title="All Types for Family: {}".format(element.Symbol.Family.Name),
    columns=selected_definitions
)

output.print_md("*Only Type Parameters are shown...*")
