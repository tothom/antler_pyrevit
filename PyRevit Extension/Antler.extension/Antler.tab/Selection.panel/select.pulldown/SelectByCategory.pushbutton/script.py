# -*- coding: utf-8 -*-

from rpw import revit, DB

from pyrevit import script
from collections import OrderedDict

import antler.forms

categories = antler.forms.select_category()
# print(categories, categories.Name)
if not categories:
	script.exit()

elements = []

# Get all Elements in Category
for category in categories:
	collector = DB.FilteredElementCollector(revit.doc).WhereElementIsNotElementType()
	collector.OfCategoryId(category.Id)
	elements.extend(collector.ToElements())

element_id_collection = List[DB.ElementId]([element.Id for element in elements])

uidoc.Selection.SetElementIds(element_id_collection)
