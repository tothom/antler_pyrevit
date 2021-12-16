from rpw import revit, DB, UI

from pyrevit import forms, script

from collections import OrderedDict
from System.Collections.Generic import List

import antler

logger = script.get_logger()

# Get selected
levels = antler.ui.preselect(revit_class=DB.Level)

logger.debug(levels)

# Select Levels
if not levels:
    levels = DB.FilteredElementCollector(revit.doc).OfCategory(
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
        elements.extend(
            antler.collectors.elements_on_level_collector(level).ToElements())

if not elements:
    logger.warning("No Elements hosted on selected Levels.")

selection = antler.ui.preselect()

# print(elements, selection)

if selection:
    selection_ids = [a.Id for a in selection]
    element_ids = [a.Id for a in elements]

    element_ids = list(set(selection_ids).intersection(set(element_ids)))

    elements = [revit.doc.GetElement(id) for id in element_ids]

element_id_collection = List[DB.ElementId](
    [element.Id for element in elements])

revit.uidoc.Selection.SetElementIds(element_id_collection)
