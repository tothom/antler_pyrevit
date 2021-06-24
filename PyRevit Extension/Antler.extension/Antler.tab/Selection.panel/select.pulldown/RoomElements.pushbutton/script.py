from System.Collections.Generic import * 
from rpw import revit, DB, UI

__doc__ = "Selects Elements generating room boundary of selected Room. Only gets Elements limiting the Room in plan, like Walls."
__title__ = "Room boundary Elements"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

def get_room_boundary_element_ids(room):
    options = DB.SpatialElementBoundaryOptions()
    
    # get boundary location from area computation settings
    boundloc = DB.AreaVolumeSettings.GetAreaVolumeSettings(doc).GetSpatialElementBoundaryLocation(DB.SpatialElementType.Room)
    options.SpatialElementBoundaryLocation = boundloc
    
    # get boundary segments
    element_ids = []
    
    for boundarylist in room.GetBoundarySegments(options):
        for boundary in boundarylist:
            element_ids.append(boundary.ElementId)
    
    return element_ids

current_selection = uidoc.Selection.GetElementIds()

#print(current_selection)

element_ids = List[DB.ElementId]()

for element_id in current_selection:

    element = doc.GetElement(element_id)
    # print(element)
    try:
        element_ids.AddRange(get_room_boundary_element_ids(element))
    except:
        pass

uidoc.Selection.SetElementIds(element_ids)