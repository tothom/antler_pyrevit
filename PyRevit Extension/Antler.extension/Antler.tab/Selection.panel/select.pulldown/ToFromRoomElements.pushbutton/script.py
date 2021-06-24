"""
Source: https://thebuildingcoder.typepad.com/blog/2009/01/filter-for-hosted-elements.html
"""


from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms

from collections import OrderedDict
from System.Collections.Generic import List

__doc__ = "All Windows and Doors going to and from a Room"
__title__ = "ToFrom Room"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc
app = revit.app

def elements_from_to_rooms(rooms, phase):
    """
    """
    collector = DB.FilteredElementCollector(doc)
    collector.OfClass(DB.FamilyInstance)
    collector.WhereElementIsNotElementType()

    elements = collector.ToElements()

    room_elements = []

    for room in rooms:
        from_room_elements = []
        to_room_elements = []

        for element in elements:

            to_room = element.ToRoom[phase]

            try:
                if element.FromRoom[phase].Id == room.Id:
                    from_room_elements.append(element)
            except:
                pass

            try:
                if element.ToRoom[phase] == room.Id:
                    to_room_elements.append(element)
            except:
                pass

        room_elements.append([from_room_elements, to_room_elements])
    return room_elements


current_selection = uidoc.Selection.GetElementIds()

element_ids = List[DB.ElementId]()

phase = doc.GetElement(uidoc.ActiveView.get_Parameter(DB.BuiltInParameter.VIEW_PHASE).AsElementId())


rooms = [doc.GetElement(a) for a in current_selection]

# for element_id in current_selection:

room_elements = elements_from_to_rooms(rooms, phase)

for elements in room_elements:

    element_ids.AddRange([e.Id for e in elements[0]])
    element_ids.AddRange([e.Id for e in elements[1]])

uidoc.Selection.SetElementIds(element_ids)
