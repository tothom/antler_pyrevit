from rpw import revit, DB#, UI
# from rpw import Transaction
# from Autodesk.Revit.DB import Transaction# , Element


from pyrevit import forms, script, EXEC_PARAMS

# from collections import OrderedDict
# from System.Collections.Generic import List

import antler
import override

logger = script.get_logger()
config = script.get_config()

def select_definition(elements, name=None):
	definitions = set()

	for element in elements:
		element_definitions = [a.Definition for a in element.Parameters]

		definitions = definitions.intersection(
			set(element_definitions)) or set(element_definitions)

	# Select definition
	definitions_dict = {a.Name: a for a in definitions}

	if name and name in definitions_dict:
		definition = definitions_dict[name]
	else:
		definition_key = forms.SelectFromList.show(
			sorted(definitions_dict.keys()),
			title="Select Instance parameter"
		) or script.exit()

		definition = definitions_dict[definition_key]

	return definition

selection = revit.uidoc.Selection.GetElementIds()


if selection:
	elements = [revit.doc.GetElement(ref) for ref in selection]


else:
	if EXEC_PARAMS.config_mode or not config.has_option('category'):
		category = antler.forms.select_category()
		config.set_option('category', category.Name)
		script.save_config()
	else:
		category = revit.doc.Settings.Categories.get_Item(config.get_option('category'))

	collector = DB.FilteredElementCollector(revit.doc, revit.uidoc.ActiveView.Id)
	collector.OfCategory(antler.util.builtin_category_from_category(category))

	elements = collector.ToElements()
	logger.debug(elements)


if EXEC_PARAMS.config_mode or not config.has_option('definition'):
	definition = select_definition(elements) or script.exit()

	config.set_option('definition', definition.Name)
	script.save_config()
else:
	definition_name = config.get_option('definition')
	definition = select_definition(elements, definition_name)




with DB.Transaction(revit.doc, __commandname__) as t:
	t.Start()

	for element in elements:
		override.override_color_by_parameter(revit.uidoc.ActiveView, element, definition)

	t.Commit()
