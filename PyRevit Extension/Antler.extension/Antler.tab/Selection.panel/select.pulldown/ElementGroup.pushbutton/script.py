"""
"""
from rpw import revit, DB
from pyrevit import script
from System.Collections.Generic import List

logger = script.get_logger()

current_selection = revit.uidoc.Selection.GetElementIds()

group_ids = List[DB.ElementId]()

for element_id in current_selection:
    element = revit.doc.GetElement(element_id)

    try:
        group_id = element.GroupId
        
        if group_id:
            group_ids.Add(group_id)
    except Exception as e:
        logger.warning(e)

revit.uidoc.Selection.SetElementIds(group_ids)
