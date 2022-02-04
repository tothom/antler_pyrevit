# -*- coding: utf-8 -*-

from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script
from collections import OrderedDict

import os
import csv
import re

import antler

logger = script.get_logger()
# schedule = forms.select_view.show()


def set_parameter_by_name(element, parameter_name, value):
	parameters = element.GetParameters(parameter_name)
	logger.debug(parameters)
	logger.debug([a.Definition.Name for a in parameters])

	# Workaround because 'Sheet Number' returns two parameters...
	if parameter_name == 'Sheet Number':
		parameters = parameters[:1]

	# logger.debug(parameters.Count)

	if parameters.Count == 1:
		parameter = parameters[0]

		if not parameter.IsReadOnly:  # parameter.UserModifiable
			# convert = PARAMETER_SET_MAPPING.get(parameter.StorageType)
			# # if convert is not None:
			# converted_value = convert(value)
			try:
				antler.parameters.set_parameter_value(parameter, value)
			except Exception as e:
				logger.debug("{} {}".format(type(e), e))
	elif parameters.Count == 0:
		logger.warning(
			"No parameters with name {} found".format(parameter_name))
	elif parameters.Count > 1:
		logger.warning(
			"Parameter name {} is ambigous and is skipped".format(parameter_name))

# Open and read CSV
file = forms.pick_file(file_ext='csv')

if not file:
	script.exit()

delimiter = forms.CommandSwitchWindow.show(
    [',', ';'],
    message='Select CSV delimiter'
)

delimiter = delimiter or ';'

with open(file, mode='r') as f:
	reader = csv.DictReader(f, delimiter=delimiter)  # , quotechar='"',
	#quoting=csv.QUOTE_MINIMAL)
	import_list = []

	for row in reader:
		import_list.append(row)

logger.debug(import_list)

# Apply changes from CSV
with DB.Transaction(revit.doc, __commandname__) as tg:
	tg.Start()

	for item in import_list:
		element_id = DB.ElementId(int(item['ElementId']))
		element = revit.doc.GetElement(element_id)
		element_type = revit.doc.GetElement(element.GetTypeId())

		logger.debug(element)

		for key, value in item.items():
			if key == 'ElementId':
				continue

			if value is None:
				continue

			pattern = '(.*)(\<.*>)'
			match = re.match(pattern, key)

			if not match:
				logger.warning("No parameter with name {} found.".format(key))
				continue

			parameter_name = match.group(1).strip()
			parameter_type = match.group(2).strip()

			logger.debug(parameter_type)
			logger.debug(parameter_name)
			logger.debug(value)

			assert parameter_type and parameter_name

			if parameter_type == '<Instance>':
				result = set_parameter_by_name(element, parameter_name, value)

			elif parameter_type == '<Type>':
				result = set_parameter_by_name(element_type, parameter_name, value)

	tg.Commit()
