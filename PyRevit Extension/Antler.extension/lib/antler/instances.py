from rpw import revit, DB
from pyrevit import forms, script

import math
import clr
import util

logger = script.get_logger()


def place_at_room_boundary(family_symbol, room, view=revit.uidoc.ActiveView, place_at_inner_boundary=False):
    """

    """
    options = DB.SpatialElementBoundaryOptions()
    options.SpatialElementBoundaryLocation = DB.SpatialElementBoundaryLocation.Finish

    boundary_segments = room.GetBoundarySegments(options)

    for segment in boundary_segments[0]:
        curve = segment.GetCurve()

        if isinstance(curve, DB.Line):
            element = revit.doc.Create.NewFamilyInstance(
                curve, family_symbol, view)
