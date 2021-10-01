from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script

from collections import OrderedDict
from System.Collections.Generic import List

import antler.util

logger = script.get_logger()

uidoc = revit.uidoc
doc = revit.doc

def get_elements_on_level(level):
    """
    """
    level_filter = DB.ElementLevelFilter(level.Id)
    collector = DB.FilteredElementCollector(doc)
    elements = collector.WherePasses(level_filter).ToElements()

    return elements

def parameter_filter(elements, parameter, parameter_value):
    for element in elements:
        element_parameter = element.get_Parameter(parameter)

def level_filter(element, level):
    element_level = None

    element_parameter = element.get_Parameter(parameter)



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

    logger.debug(level_keys)

    levels = [levels_dict.get(key) for key in level_keys]

logger.debug(levels)

# print(len(elements))

elements = []

if levels:
    for level in levels:
        elements.extend(get_elements_on_level(level))


selection = antler.util.preselect()

# print(elements, selection)

if selection:
    selection_ids = [a.Id for a in selection]
    element_ids = [a.Id for a in elements]

    element_ids = list(set(selection_ids).intersection(set(element_ids)))

    elements = [doc.GetElement(id) for id in element_ids]

element_id_collection = List[DB.ElementId](
    [element.Id for element in elements])

uidoc.Selection.SetElementIds(element_id_collection)
