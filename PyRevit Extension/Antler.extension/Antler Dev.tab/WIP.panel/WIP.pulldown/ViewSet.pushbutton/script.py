# -*- coding: utf-8 -*-
from rpw import revit, DB, UI

from pyrevit import forms
from collections import OrderedDict

from System.Windows import Clipboard

import csv
import json

__doc__ = "Create View Set"
__title__ = "Create View Set"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

# Get open views
current_selected_sheets = revit.get_selection().include(DB.ViewSheet).elements

view_set = DB.ViewSet()

for sheet in current_selected_sheets:
    view_set.Insert(sheet)
