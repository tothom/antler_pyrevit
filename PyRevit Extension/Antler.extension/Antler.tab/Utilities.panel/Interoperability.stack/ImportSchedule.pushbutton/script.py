# -*- coding: utf-8 -*-

from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script
from collections import OrderedDict

import os
import csv
import re

logger = script.get_logger()
# schedule = forms.select_view.show()

PARAMETER_SET_MAPPING = {
	# The internal data is stored in the form of a signed 32 bit integer.
	DB.StorageType.Integer: int,
	# float, # The data will be stored internally in the form of an 8 byte floating point number.
	DB.StorageType.Double: None,
	# The internal data will be stored in the form of a string of characters.
	DB.StorageType.String: str,
	# The data type represents an element and is stored as the id of the element.
	DB.StorageType.ElementId: None,
}

PARAMETER_UNIT_CONVERSION = {
	DB.ParameterType.Length: 304.8,
}


def set_parameter(element, parameter_name, value):
	parameters = element.GetParameters(parameter_name)
	logger.debug(parameters)
	logger.debug([a.Definition.Name for a in parameters])

	# Workaround for because 'Sheet number' returns two parameters...
	if parameter_name == 'Sheet Number':
		parameters = [parameters[0]]

	# logger.debug(parameters.Count)

	if parameters.Count == 1:
		parameter = parameters[0]
		if not parameter.IsReadOnly:  # parameter.UserModifiable
			convert = PARAMETER_SET_MAPPING.get(parameter.StorageType)

			if convert:
				converted_value = convert(value)
				try:
					result = parameter.Set(converted_value)
				except Exception as e:
					logger.warning("{} {}".format(type(e), e))
	else:
		logger.warning(
			"Parameter name {} is ambigous and is skipped".format(parameter_name))


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


with DB.Transaction(revit.doc, __commandname__) as tg:
	tg.Start()

	for item in import_list:
		element_id = DB.ElementId(int(item['ElementId']))
		element = revit.doc.GetElement(element_id)
		element_type = revit.doc.GetElement(element.GetTypeId())

		logger.debug(element)

		for key, value in item.items():
			logger.debug(value)

			if key == 'ElementId':
				continue

			if not value:
				continue

			pattern = '(\<.*>\s)(.*)'
			match = re.match(pattern, key)

			parameter_type = match.group(1).strip()
			parameter_name = match.group(2)

			logger.debug(parameter_type)
			logger.debug(parameter_name)

			assert parameter_type and parameter_name

			if parameter_type == '<Instance>':
				result = set_parameter(element, parameter_name, value)

			elif parameter_type == '<Type>':
				result = set_parameter(element_type, parameter_name, value)

	tg.Commit()
