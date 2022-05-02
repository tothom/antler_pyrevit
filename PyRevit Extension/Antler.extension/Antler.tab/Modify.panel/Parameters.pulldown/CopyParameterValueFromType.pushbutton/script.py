from rpw import revit, DB, UI

from pyrevit import forms, script

# from collections import OrderedDict
from System.Collections.Generic import List

import antler

logger = script.get_logger()


type_parameter_name = forms.ask_for_string(
	prompt="Enter Type Parameter name",
	).strip()


collector = DB.FilteredElementCollector(revit.doc).WhereElementIsNotElementType()
elements = collector.ToElements()



instance_definitions = antler.parameters.get_all_definitions(
	elements)
# instance_definitions = antler.parameters.get_definitions_from_elements(
# 	elements)

instance_definition_identifier = forms.SelectFromList.show(
	sorted(instance_definitions.keys()),
	title='Select Instance Parameters',
	multiselect=False
)

instance_definition = instance_definitions[instance_definition_identifier]
#
# instance_definition_identifier = forms.ask_for_string(
# 	prompt="Enter Instance Parameter name",
# 	).strip()


with DB.Transaction(revit.doc, __commandname__) as t:
	t.Start()

	for element in elements:

		element_type = revit.doc.GetElement(element.GetTypeId())

		if not element_type:
			continue

		type_parameter = element_type.LookupParameter(type_parameter_name)

		if not type_parameter:
			continue

		# instance_parameter = element.LookupParameter(instance_parameter_name)
		instance_parameter = element.get_Parameter(instance_definition)

		if not instance_parameter:
			continue

		try:
			type_parameter_value = antler.parameters.get_parameter_value(type_parameter)

			if type_parameter_value is None:
				type_parameter_value = ''

			antler.parameters.set_parameter_value(instance_parameter, type_parameter_value)
		except Exception as e:
			logger.warning((type(e), e))
		else:
			# print("Value {} wrote to instance".format(type_parameter_value))
			pass

	t.Commit()
