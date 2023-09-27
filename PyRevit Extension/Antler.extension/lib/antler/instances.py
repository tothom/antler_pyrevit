from rpw import revit, DB
from pyrevit import forms, script

import math
import clr
import utils

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
            
def place_wall_at_room_boundary(wall_type, room, height=1):
    options = DB.SpatialElementBoundaryOptions()
    options.SpatialElementBoundaryLocation = DB.SpatialElementBoundaryLocation.Finish

    boundary_segments = room.GetBoundarySegments(options)

    offset = wall_type.Width / 2

    for segment in boundary_segments[0]:
        curve = segment.GetCurve()

        if isinstance(curve, DB.Line):
            if curve.ApproximateLength < 1:
                continue

            curve = curve.CreateOffset(offset, DB.XYZ(0,0,-1))

            wall = DB.Wall.Create(
                room.Document,
                curve,
                wall_type.Id,
                room.Level.Id,
                height,
                0,
                False,
                False
            )


def filled_region_from_room(filled_region_type, room, view=revit.uidoc.ActiveView, doc=revit.doc):
    """

    """
    crv_loops = geometry.crv_loops_from_room(room)

    element = DB.FilledRegion.Create(doc, filled_region_type.Id, view.Id, crv_loops)

    return element


def count_elements_of_type(element_type):
    instances = antler.collectors.get_instances_of_element_type(element_type)

    return len(instances)
