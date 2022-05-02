from rpw import revit, DB, UI

from pyrevit import forms, script

# from collections import OrderedDict
# from System.Collections.Generic import List

import antler

logger = script.get_logger()


# Select category
category = antler.forms.select_category()

collector = DB.FilteredElementCollector(revit.doc)
collector.OfCategory(antler.util.builtin_category_from_category(category))

collector.WhereElementIsNotElementType()  # .ToElements()

elements = collector.ToElements()


if not elements:
	script.exit()

definitions = set()

for element in elements:
	element_definitions = [a.Definition for a in element.Parameters]

	definitions = definitions.intersection(
		set(element_definitions)) or set(element_definitions)

# Select definition
definitions_dict = {a.Name: a for a in definitions}

source_key = forms.SelectFromList.show(
	sorted(definitions_dict.keys()),
	title="Select Instance parameter to copy from"
)

if not source_key:
	script.exit()

source_definition = definitions_dict[source_key]

# filtered_definitions_dict = [k: v for k, v in definitions_dict.items() if v.ParameterType == source_definition.ParameterType]
filtered_definitions_dict = dict(filter(
	lambda x: x[1].ParameterType == source_definition.ParameterType,  definitions_dict.items()))

destination_key = forms.SelectFromList.show(
	sorted(filtered_definitions_dict.keys()),
	title="Select Instance parameter to copy from"
)

if not destination_key:
	script.exit()

destination_definition = definitions_dict[destination_key]

logger.info(source_definition)
logger.info(destination_definition)

parameter_value_type_mapping = {

}


with DB.Transaction(revit.doc, __commandname__) as t:
	t.Start()

	for element in elements:
		source_parameter = element.get_Parameter(source_definition)
		destination_parameter = element.get_Parameter(destination_definition)

		if source_parameter.HasValue:
			logger.info(source_parameter)
			logger.info(destination_parameter)

			logger.info("Source")

			logger.info("{value}, {storage_type}".format(
				value=source_parameter.AsValueString(),
				storage_type=source_parameter.StorageType)
				)

			logger.info("Destination")

			logger.info("{value}, {storage_type}".format(
				value=destination_parameter.AsValueString(),
				storage_type=destination_parameter.StorageType)
				)
			try:
				pass
			except Exception as e:
				logger.info(e)

				# destination_parameter.s

	t.Commit()
