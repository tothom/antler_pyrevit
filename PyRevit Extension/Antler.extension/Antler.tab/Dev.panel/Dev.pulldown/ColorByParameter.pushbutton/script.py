from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script

from collections import OrderedDict
from System.Collections.Generic import List

import antler

logger = script.get_logger()


def override_color_by_parameter(view, element, parameter):
	element_parameter = element.get_Parameter(parameter)

	parameter_value = element_parameter.AsString() or element_parameter.AsValueString()

	logger.debug(parameter_value)

	if parameter_value is not None:
		line_color = antler.color.random_hsv_color(
			seed=parameter_value, s=0.7, v=0.7)
		fill_color = antler.color.relative_color_hsv(line_color, dv=+0.2)

		logger.debug(line_color)
		logger.debug(fill_color)

		antler.view.override_element_color(
				element, view, fill_color=fill_color, line_color=line_color)
	else:
		antler.view.override_element_color(
				element, view)


category = antler.ui.select_category()

collector = DB.FilteredElementCollector(revit.doc, revit.uidoc.ActiveView.Id)
collector.OfCategory(antler.util.builtin_category_from_category(category))

elements = collector.WhereElementIsNotElementType().ToElements()

definitions = set()

for element in elements:
	element_definitions = [a.Definition for a in element.Parameters]

	definitions = definitions.intersection(
		set(element_definitions)) or set(element_definitions)

# Select definition
definitions_dict = {a.Name: a for a in definitions}

definition_key = forms.SelectFromList.show(
	sorted(definitions_dict.keys()),
	title="Select Instance parameter"
)

definition = definitions_dict[definition_key]

with DB.Transaction(revit.doc, __commandname__) as t:
	t.Start()

	for element in elements:
		override_color_by_parameter(revit.uidoc.ActiveView, element, definition)

	t.Commit()
#
# element_id_collection = List[DB.ElementId](
# 	[element.Id for element in elements])

# uidoc.Selection.SetElementIds(element_id_collection)
