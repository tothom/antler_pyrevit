from rpw import revit, DB
from pyrevit import forms, script

import clr
from collections import OrderedDict

import util
import collectors

"""
All functions which is related to UI, except forms, which may be found in
forms.py.
"""

logger = script.get_logger()


def preselect(revit_class=()):
    selected_element_ids = revit.uidoc.Selection.GetElementIds()

    filtered_elements = []

    for element_id in selected_element_ids:
        element = revit.doc.GetElement(element_id)

        if isinstance(element, revit_class) or not revit_class:
            filtered_elements.append(element)

    return filtered_elements
