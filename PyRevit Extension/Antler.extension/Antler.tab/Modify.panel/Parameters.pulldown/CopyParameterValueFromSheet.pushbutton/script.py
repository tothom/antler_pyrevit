from rpw import revit, DB, UI

from pyrevit import forms, script

# from collections import OrderedDict
from System.Collections.Generic import List

import antler

logger = script.get_logger()



# views = forms.select_views()
views = antler.ui.preselect((DB.View, ))

parameter_ids = DB.ParameterFilterUtilities.GetFilterableParametersInCommon(
	revit.doc, List[DB.ElementId]([
		DB.ElementId(DB.BuiltInCategory.OST_Sheets),
		DB.ElementId(DB.BuiltInCategory.OST_Views),
		]))

logger.debug(parameter_ids)

parameters = [revit.doc.GetElement(a) for a in parameter_ids]

parameters = [a for a in parameters if a]

logger.debug(parameters)

from_parameter_element = antler.forms.select_elements(
	parameters,
	naming_function=lambda x: x.GetDefinition().Name,
	multiselect=False
	) or script.exit()

logger.debug(from_parameter_element)

from_definition = from_parameter_element.GetDefinition()


with DB.Transaction(revit.doc, __commandname__) as t:
	t.Start()

	for view in views:
		try:
			sheet_number_parameter = view.get_Parameter(
				DB.BuiltInParameter.VIEWPORT_SHEET_NUMBER)

			logger.debug(sheet_number_parameter.StorageType)
			logger.debug(sheet_number_parameter.HasValue)

			if sheet_number_parameter.HasValue:
				sheet_number = sheet_number_parameter.AsString()

				logger.debug(sheet_number)

				sheet = antler.collectors.get_sheet_by_number(sheet_number)

				from_parameter = sheet.get_Parameter(from_definition)

				to_parameter = view.LookupParameter(from_definition.Name)

				to_parameter.Set(from_parameter.AsString())
		except Exception as e:
			logger.warning((type(e), e))

	t.Commit()
