from rpw import revit, DB, UI

from pyrevit import forms, script

# from collections import OrderedDict
# from System.Collections.Generic import List

import antler

logger = script.get_logger()

elements = antler.ui.preselect()

phase_parameter = revit.uidoc.ActiveView.get_Parameter(DB.BuiltInParameter.VIEW_PHASE)
phase_id = phase_parameter.AsElementId()

room = antler.collectors.room_collector(phase_id=phase_id).FirstElement()

from_parameter = forms.select_parameters(room, multiselect=False)


with DB.Transaction(revit.doc, __commandname__) as t:
	t.Start()

	for element in elements:
		room = element.Room

	t.Commit()
