# -*- coding: utf-8 -*-

from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms
from collections import OrderedDict

import os
import csv
import json


__doc__ = "Select Elements by Category"
__title__ = "Select By Category"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

def select_categories():
	categories_dict = {c.Name: c for c in doc.Settings.Categories}
	result = forms.SelectFromList.show(sorted(categories_dict.keys()), multiselect=True)

	return [categories_dict[a] for a in result]

categories = select_categories()
# print(categories, categories.Name)

if categories:
	elements = []

	# Get all Elements in Category
	for category in categories:
		element_collector = DB.FilteredElementCollector(doc).WhereElementIsNotElementType().OfCategoryId(category.Id)
		elements.extend(element_collector.ToElements())


	element_id_collection = List[DB.ElementId]([element.Id for element in elements])

	uidoc.Selection.SetElementIds(element_id_collection)
