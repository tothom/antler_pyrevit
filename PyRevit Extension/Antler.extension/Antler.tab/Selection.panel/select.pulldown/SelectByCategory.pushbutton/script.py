# -*- coding: utf-8 -*-

from rpw import revit, DB

from pyrevit import script, forms
from collections import OrderedDict
from System.Collections.Generic import List

import antler.forms
from antler import LOGGER

import time

output = script.get_output()

categories = antler.forms.select_category(multiselect=True)
# print(categories, categories.Name)
if not categories:
	script.exit()

elements = []

# Get all Elements in Category
for category in categories:
	collector = DB.FilteredElementCollector(revit.doc).WhereElementIsNotElementType()
	collector.OfCategoryId(category.Id)
	elements.extend(collector.ToElements())

LOGGER.debug(elements)

if not elements:
	# forms.toast("No elements found.")
	#forms.alert("No elements found.")
	output.resize(400, 400)
	print("No elements found.")
	# time.sleep(5)
	output.self_destruct(2)

element_id_collection = List[DB.ElementId]([element.Id for element in elements])

revit.uidoc.Selection.SetElementIds(element_id_collection)
