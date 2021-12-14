"""
Source: https://thebuildingcoder.typepad.com/blog/2009/01/filter-for-hosted-elements.html
"""
from rpw import revit, DB
from pyrevit import script
from System.Collections.Generic import List

import antler.collectors

logger = script.get_logger()

current_selection = revit.uidoc.Selection.GetElementIds()

#print(current_selection)

element_ids = List[DB.ElementId]()

for element_id in current_selection:

    host_element = revit.doc.GetElement(element_id)
    hosted_elements = antler.collectors.hosted_by_collector(host_element).ToElements()

    logger.debug(hosted_elements)

    [element_ids.Add(e.Id) for e in hosted_elements]

revit.uidoc.Selection.SetElementIds(element_ids)
