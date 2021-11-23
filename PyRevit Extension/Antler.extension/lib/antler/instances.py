from rpw import revit, DB
from pyrevit import forms, script

import math
import clr
import util

import geometry

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
            if curve.ApproximateLength < 1:
                continue
            element = revit.doc.Create.NewFamilyInstance(
                curve, family_symbol, view)


def filled_region_from_room(filled_region_type, room, view=revit.uidoc.ActiveView, doc=revit.doc):
    """

    """
    crv_loops = geometry.crv_loops_from_room(room)

    element = DB.FilledRegion.Create(doc, filled_region_type.Id, view.Id, crv_loops)

    return element
