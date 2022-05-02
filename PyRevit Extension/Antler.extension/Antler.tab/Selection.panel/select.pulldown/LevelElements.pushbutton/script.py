from rpw import revit, DB, UI

from pyrevit import forms, script

from collections import OrderedDict
from System.Collections.Generic import List

import antler

logger = script.get_logger()

# Get selected
levels = antler.ui.preselect(revit_class=DB.Level) or antler.forms.select_levels() or script.exit()

logger.debug(levels)


elements = []

for level in levels:
    elements.extend(
        antler.collectors.elements_on_level_collector(level).ToElements())

if not elements:
    logger.warning("No Elements hosted on selected Levels.")

# selection = antler.ui.preselect()

# print(elements, selection)

# if selection:
#     selection_ids = [a.Id for a in selection]
#     element_ids = [a.Id for a in elements]
#
#     element_ids = list(set(selection_ids).intersection(set(element_ids)))
#
#     elements = [revit.doc.GetElement(id) for id in element_ids]

element_id_collection = List[DB.ElementId](
    [element.Id for element in elements])

revit.uidoc.Selection.SetElementIds(element_id_collection)
