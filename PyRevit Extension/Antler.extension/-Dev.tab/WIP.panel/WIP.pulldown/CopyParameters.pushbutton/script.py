from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms

from collections import OrderedDict
from System.Collections.Generic import List

__doc__ = "Copy Parameter values from one parameter to another."
__title__ = "Copy Parameters"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc



# Select Levels
levels = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
levels_dict = {"{} ({})".format(level.Name, level.Elevation): level for level in levels}

levels_dict = OrderedDict(sorted(levels_dict.items(), key=lambda (key, value): value.Elevation, reverse=True))
level_key = forms.SelectFromList.show(levels_dict.keys(), button_name='Select Level', multiple=False, message='Select level to change to.')
level = levels_dict.get(level_key) # Using get() to avoid error message when cancelling dialog.
# levels = forms.select_levels()

elements = []

if level:
	# for level in levels:
	elements.extend(get_elements_on_level(level))

element_id_collection = List[DB.ElementId]([element.Id for element in elements])

uidoc.Selection.SetElementIds(element_id_collection)
