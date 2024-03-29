import antler

from rpw import revit, DB

from pyrevit import forms, script, EXEC_PARAMS


logger = script.get_logger()
# config = script.get_config()

elements = antler.ui.preselect()

if not elements:
	collector = DB.FilteredElementCollector(revit.doc, revit.uidoc.ActiveView.Id)
	collector.WhereElementIsNotElementType()

	elements = collector.ToElements()

empty_override = DB.OverrideGraphicSettings()

with DB.Transaction(revit.doc, __commandname__) as t:
	t.Start()

	for element in elements:
		revit.uidoc.ActiveView.SetElementOverrides(element.Id, empty_override)

	t.Commit()
