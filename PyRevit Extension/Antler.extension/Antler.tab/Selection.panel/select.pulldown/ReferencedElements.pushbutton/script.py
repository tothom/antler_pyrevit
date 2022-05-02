"""
"""
from rpw import revit, DB
from System.Collections.Generic import List

current_selection = revit.uidoc.Selection.GetElementIds()

#print(current_selection)

element_ids = List[DB.ElementId]()

for element_id in current_selection:

    element = revit.doc.GetElement(element_id)
    # if isinstance(element, DB.Dimension)
    # references = element.References

    for reference in element.References:

        # linked_element_id = reference.LinkedElementId
        # element_id = reference.

        element_ids.Add(reference.ElementId)

revit.uidoc.Selection.SetElementIds(element_ids)
