# -*- coding: utf-8 -*-

from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms
from collections import OrderedDict

import os
import csv
import json


__doc__ = "Report of all links in project"
__title__ = "Links Report"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

# Get Revit Links, including IFC




# Get DWG Links




# Other links?




def select_categories():
	categories_dict = {c.Name: c for c in doc.Settings.Categories}
	result = forms.SelectFromList.show(sorted(categories_dict.keys()), multiselect=True)

	return [categories_dict[a] for a in result]

categories = select_categories()
# print(categories, categories.Name)

type_elements = []
parameters = set()

# Get all Types in Category
for category in categories:
	type_collector = DB.FilteredElementCollector(doc).WhereElementIsElementType().OfCategoryId(category.Id)
	elements = type_collector.ToElements()
	type_elements.extend(elements)

	parameters_map = elements[0].ParametersMap
	parameters |= set([parameter.Definition.Name for parameter in parameters_map])

parameters_selected = forms.SelectFromList.show(sorted(parameters), multiselect=True)

# print(parameters_selected)

element_list = []

# Iterate Element Type list and write information to dictionary.
for element in type_elements:
	# print(element)
	# in_place = element.IsInPlace
    # Try get Category name
	try:
		category = element.Category.Name
	except:
		category = None

    # Count all Elements of type
	bip = DB.BuiltInParameter.ELEM_FAMILY_PARAM
	provider = DB.ParameterValueProvider(DB.ElementId(bip))
	evaluator = DB.FilterNumericEquals()

	rule = DB.FilterElementIdRule(provider, evaluator, element.Id)
	filter = DB.ElementParameterFilter(rule)
	collector = DB.FilteredElementCollector(doc).WherePasses(filter)

	count = collector.GetElementCount()

    # Get Type name
	name = element.LookupParameter("Type Name").AsString()

    # Write information to dictionary
	information = {
		'Id': element.Id.IntegerValue,
		'Category': category,
		'Family': element.FamilyName,
		'Type': name,
		'Count':count
		}

	for parameter in parameters_selected:
		# print(parameter)
		values = element.GetParameters(parameter)

		if values:
			information[parameter] = values[0].AsValueString()
		else:
			information[parameter] = None

	element_list.append(information)

# for item in element_list:
# 	print(item)
export_dict = {'types': element_list}

def write_csv(data, file):
	# print('CSV')
	writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	writer.writerow(export_dict['types'][0].keys())
	# ['id', 'category', 'family', 'type', 'count'])

	for element in export_dict['types']:
		writer.writerow(element.values())

# 		sequence = [key] + list(value)
# 		print(sequence)
# 		writer.writerow(sequence)

def write_json(data, file):
	# print('JSON')
	json.dump(data, file, ensure_ascii=False)

write_format_mapper = {
'.csv': write_csv,
'.json': write_json
}

# Write File
file = forms.save_file()

with open(file, mode='wb') as f:
	name, ext = os.path.splitext(file)
	write_format_mapper.get(ext)(export_dict, f)
