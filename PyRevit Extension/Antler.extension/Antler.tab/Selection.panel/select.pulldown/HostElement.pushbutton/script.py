"""
"""
from rpw import revit, DB
from System.Collections.Generic import List

current_selection = revit.uidoc.Selection.GetElementIds()

#print(current_selection)

element_ids = List[DB.ElementId]()

for element_id in current_selection:

    element = revit.doc.GetElement(element_id)
    host_element = element.Host

    element_ids.Add(host_element.Id)

revit.uidoc.Selection.SetElementIds(element_ids)
