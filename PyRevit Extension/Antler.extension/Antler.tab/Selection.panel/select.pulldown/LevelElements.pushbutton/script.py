from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script

from collections import OrderedDict
from System.Collections.Generic import List

import antler.util

logger = script.get_logger()

__doc__ = "Gets all Elements hosted by a Level"
__title__ = "Elements on Level"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

def get_elements_on_level(level):
    """
    """
    level_filter = DB.ElementLevelFilter(level.Id)
    collector = DB.FilteredElementCollector(doc)
    elements = collector.WherePasses(level_filter).ToElements()

    return elements

# Get selected
levels = antler.util.preselect(revit_class=DB.Level)

logger.debug(levels)

# Select Levels
if not levels:
    levels = DB.FilteredElementCollector(doc).OfCategory(
        DB.BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
    levels_dict = {"{} ({})".format(
        level.Name, level.Elevation): level for level in levels}

    levels_dict = OrderedDict(sorted(levels_dict.items(), key=lambda (key, value): value.Elevation, reverse=True))
    level_keys = forms.SelectFromList.show(levels_dict.keys(
    ), button_name='Select Level', multiselect=True, message='Select level to change to.')
    print(level_keys)

    levels = [levels_dict.get(key) for key in level_keys]

logger.debug(levels)

elements = []

if levels:
    for level in levels:
        elements.extend(get_elements_on_level(level))

element_id_collection = List[DB.ElementId](
    [element.Id for element in elements])

uidoc.Selection.SetElementIds(element_id_collection)
