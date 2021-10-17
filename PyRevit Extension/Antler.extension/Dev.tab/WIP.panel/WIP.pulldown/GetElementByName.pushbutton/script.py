# -*- coding: utf-8 -*-

from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms
from collections import OrderedDict

import csv
import json

import time

__doc__ = ""
__title__ = "Elements By Name"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

def get_element_by_name(name, hint=None):
	"""
	"""

	# TODO: Change class
	elements = DB.FilteredElementCollector(doc).OfClass(DB.Material).ToElements()
	elements = filter(lambda e:e.Name == name, elements)

	return elements

name = forms.ask_for_string(
	prompt="Enter name to search for",
	title="Search name"
	)

t = time.time()

elements = get_element_by_name(name)

# print(time.time() - t)

element_ids = List[DB.ElementId]()

for element in elements:
    element_ids.Add(element.Id)

uidoc.Selection.SetElementIds(List[DB.ElementId]([element.Id for element in elements]))
