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


def select_family_types():
	fam_type_collector = DB.FilteredElementCollector(
		doc).WhereElementIsElementType().OfClass(DB.FamilySymbol)
	fam_types = fam_type_collector.ToElements()

	fam_types_dict = OrderedDict()

	# print(dir(fam_types[0]))
	# print(fam_types)

	for fam_type in fam_types:
		symbol_name = fam_type.get_Parameter(
			DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
		family_name = fam_type.FamilyName

		family_type_name = "{0} - {1}".format(family_name, symbol_name)

		fam_types_dict[family_type_name] = fam_type

	selected = forms.SelectFromList.show(
		sorted(fam_types_dict.keys()), multiselect=True)

	if selected:
		return [fam_types_dict[key] for key in selected]
	else:
		return []

family_types = select_family_types()
# print(family_types)
elements = []

if family_types:
	for family_type in family_types:
		filter = DB.FamilyInstanceFilter(doc, family_type.Id)
		collector = DB.FilteredElementCollector(doc).WhereElementIsNotElementType().WherePasses(filter)

		elements.extend(collector.ToElements())

	# print(elements)

	element_id_collection = List[DB.ElementId]([element.Id for element in elements])

	uidoc.Selection.SetElementIds(element_id_collection)
