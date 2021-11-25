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

view_schedule = revit.uidoc.ActiveView

elements = DB.FilteredElementCollector(
	revit.doc, view_schedule.Id).WhereElementIsNotElementType().ToElements()

logger.info(elements)

schedule_definition = view_schedule.Definition

parameter_ids = []

for field_index in range(schedule_definition.GetFieldCount()-1):
	schedule_field = schedule_definition.GetField(field_index)

	parameter_id = schedule_field.ParameterId  # .ToString()
	logger.info(parameter_id)

	if parameter_id:
		parameter_ids.append(parameter_id)

# table_data = view_schedule.GetTableData()
#
# for section_index in table_data.NumberOfSections:
# 	logger.info(section_index)
# 	section_data = table_data.GetSectionData(section_index)
# 	logger.info(section_data)
# 	param_id = section_data.Get

# result = table_data.GetSectionData(sectiontype)

export_list = []

for element in elements:
	element_dict = {}
	element_dict['ElementId'] = element.Id.ToString()

	for parameter_id in parameter_ids:
		logger.info(parameter_id)
		# parameter = element.get_Parameter(parameter_id)
		parameter = revit.doc.GetElement(parameter_id)
		logger.info(parameter)
		# element_dict[parameter.Definition.Name] = parameter.AsValueString()

	export_list.append(element_dict)

logger.info(export_list)


def write_csv(data, file):
	# print('CSV')
	writer = csv.writer(f, delimiter=';', quotechar='"',
	                    quoting=csv.QUOTE_MINIMAL)

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
# file = forms.save_file()
#
# with open(file, mode='wb') as f:
# 	name, ext = os.path.splitext(file)
# 	write_format_mapper.get(ext)(export_dict, f)
