from rpw import revit, DB
from pyrevit import forms, script

import math
import clr
# import frange
import util

logger = script.get_logger()


def transform_z_rotation(transform):
    """
    Extracts rotation around z-axis for given transform.
    """
    transform_x_vector = transform.OfVector(DB.XYZ.BasisX)

    angle = math.atan(transform_x_vector.Y, transform_x_vector.X)

    return angle


def orient_on_xy_plane(from_plane, to_plane):
    """
    """
    # Translate
    translation_vector = DB.XYZ(
        to_plane.Origin.X - from_plane.Origin.X,
        to_plane.Origin.X - from_plane.Origin.X,
        to_plane.Origin.X - from_plane.Origin.X,
    )

    # Rotate
    from_angle = transform_z_rotation(from_plane)
    to_angle = transform_z_rotation(to_plane)

    delta_angle = to_angle - from_angle


def orient_to_plane(element, plane):
    """
    Orients element to plane
    """
    # Create


def element_direction(element):
    """
    Returns direction of element as XYZ. For a wall it will return the running direction of the wall.
    """
    # First try. Works on grids.
    try:
        line = clr.Convert(element.Curve, DB.Line)
        direction = line.Direction
        return direction
    except Exception as e:
        logger.debug(e)

    # Second try. Works on line based elements such as Walls. Will not work if Wall is curved.
    try:
        location_crv = clr.Convert(element.Location, DB.LocationCurve)
        line = clr.Convert(location_crv.Curve, DB.Line)
        direction = line.Direction
        return direction
    except Exception as e:
        logger.debug(e)

    # Third try. Works on FamilyInstances.
    try:
        direction = element.FacingOrientation
        return direction
    except Exception as e:
        logger.debug(e)

    logger.warning("Failed to get direction from {element}".format(element=element))
    return None


def element_centre_point(element):
    """
    """
    if isinstance(element, (DB.Wall)):
        location_crv = clr.Convert(element.Location, DB.LocationCurve)
        centre_pt = location_crv.Curve.Evaluate(0.5, True)
    elif isinstance(element, (DB.FamilyInstance)):
        return element.Location.Point
    else:
        message = "Centre point for type {} not yet supported".format(
            type(element))
        # logger.debug(message)
        raise TypeError(message)

    return centre_pt


def straighten_element(
        element,
        guides,
        axis_pt=None,
        normal=DB.XYZ(0, 0, 1),
        angle_snap=math.pi,
        doc=revit.doc):

    direction = element_direction(element)

    angle_snap = angle_snap or math.pi # Cannot be 0

    angles = []

    for guide in guides:
        angle = direction.AngleOnPlaneTo(guide, normal)
        additions = util.drange(0, math.pi, angle_snap)
        angles.extend([angle + a for a in additions])

    logger.debug(angles)

    angle = sorted(angles, key=lambda x: abs(math.sin(x)))[0]
    rotation_angle = math.atan(math.tan(angle))

    if rotation_angle == 0:
        return element

    if axis_pt:
        axis =  DB.Line.CreateUnbound(axis_pt, normal)
    else:
        centre_pt = element_centre_point(element)
        axis = DB.Line.CreateUnbound(centre_pt, normal)

    DB.ElementTransformUtils.RotateElement(
        doc, element.Id, axis, rotation_angle)

    return element
