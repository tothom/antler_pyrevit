# -*- coding: utf-8 -*-

from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script
from collections import OrderedDict

import os
import csv
import json

logger = script.get_logger()
# schedule = forms.select_view.show()

def build_csv_file_header():
	pass

def element_to_dict():
	pass

def build_csv_data(elements, include_parameter_ids):
	export_list = []

	for element in elements:
		element_dict = {}

		element_dict['ElementId'] = element.Id.ToString()

		for parameter in element.Parameters:
			# logger.debug(parameter.Definition.Name)
			# logger.debug(parameter.Id)
			if parameter.Id in field_parameter_ids:
				logger.debug(parameter.Id)
				# logger.debug(parameter.AsValueString())
				element_dict['<Instance> '+parameter.Definition.Name] = parameter.AsString() or parameter.AsValueString()
				#logger.debug(parameter.Id in field_parameter_ids)

		element_type = revit.doc.GetElement(element.GetTypeId())

		logger.debug(element_type)

		if element_type:
			for parameter in element_type.Parameters:
				if parameter.Id in field_parameter_ids:
					logger.debug(parameter.Id)
					# logger.debug(parameter.AsValueString())
					element_dict['<Type> '+parameter.Definition.Name] = parameter.AsString() or parameter.AsValueString()

		# for parameter_id in field_parameter_ids:
		# 	logger.debug(parameter_id)
		# 	# parameter = element.get_Parameter(parameter_id)
		# 	parameter = revit.doc.GetElement(parameter_id)
		# 	logger.debug(parameter)
			# element_dict[parameter.Definition.Name] = parameter.AsValueString()

		export_list.append(element_dict)


view_schedule = revit.uidoc.ActiveView

elements = DB.FilteredElementCollector(
	revit.doc, view_schedule.Id).WhereElementIsNotElementType().ToElements()

logger.debug(elements)

schedule_definition = view_schedule.Definition

field_parameter_ids = []

for field_index in range(schedule_definition.GetFieldCount()):
	schedule_field = schedule_definition.GetField(field_index)

	parameter_id = schedule_field.ParameterId  # .ToString()

	if parameter_id:
		field_parameter_ids.append(parameter_id)

# table_data = view_schedule.GetTableData()
#
# for section_index in table_data.NumberOfSections:
# 	logger.debug(section_index)
# 	section_data = table_data.GetSectionData(section_index)
# 	logger.debug(section_data)
# 	param_id = section_data.Get

# result = table_data.GetSectionData(sectiontype)

logger.debug(field_parameter_ids)

export_list = []

for element in elements:
	element_dict = {}

	element_dict['ElementId'] = element.Id.ToString()

	for parameter in element.Parameters:
		# logger.debug(parameter.Definition.Name)
		# logger.debug(parameter.Id)
		if parameter.Id in field_parameter_ids:
			logger.debug(parameter.Id)
			# logger.debug(parameter.AsValueString())
			element_dict['<Instance> '+parameter.Definition.Name] = parameter.AsString() or parameter.AsValueString()
			#logger.debug(parameter.Id in field_parameter_ids)

	element_type = revit.doc.GetElement(element.GetTypeId())

	logger.debug(element_type)

	if element_type:
		for parameter in element_type.Parameters:
			if parameter.Id in field_parameter_ids:
				logger.debug(parameter.Id)
				# logger.debug(parameter.AsValueString())
				element_dict['<Type> '+parameter.Definition.Name] = parameter.AsString() or parameter.AsValueString()

	# for parameter_id in field_parameter_ids:
	# 	logger.debug(parameter_id)
	# 	# parameter = element.get_Parameter(parameter_id)
	# 	parameter = revit.doc.GetElement(parameter_id)
	# 	logger.debug(parameter)
		# element_dict[parameter.Definition.Name] = parameter.AsValueString()

	export_list.append(element_dict)

logger.debug(export_list)


# Write File
filename = "{doc_title} - {view_title}".format(
	doc_title=revit.doc.Title,
	view_title=view_schedule.Title
	).replace(':', ' -')

file = forms.save_file(file_ext='csv', default_name=filename)

if not file:
	script.exit()

keys = set().union(*(d.keys() for d in export_list))

with open(file, mode='wb') as f:
    w = csv.DictWriter(f, keys, delimiter=';', quotechar='"',
						quoting=csv.QUOTE_MINIMAL)
    w.writeheader()
    w.writerows(export_list)
