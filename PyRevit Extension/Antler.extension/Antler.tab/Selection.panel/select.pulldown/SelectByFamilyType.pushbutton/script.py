# -*- coding: utf-8 -*-

from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms
from collections import OrderedDict

__doc__ = "Select Elements by Family Type"
__title__ = "Select By Family Type"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc


family_types = select_family_types()
# print(family_types)
elements = []

if family_types:
	for family_type in family_types:
		filter = DB.FamilyInstanceFilter(doc, family_type.Id)
		collector = DB.FilteredElementCollector(
			doc).WhereElementIsNotElementType().WherePasses(filter)

		elements.extend(collector.ToElements())

	# print(elements)

	element_id_collection = List[DB.ElementId](
		[element.Id for element in elements])

	uidoc.Selection.SetElementIds(element_id_collection)
