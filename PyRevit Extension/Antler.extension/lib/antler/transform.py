from rpw import revit, DB
from pyrevit import forms, script

import math
import clr

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
    if isinstance(element, (DB.Grid)):
        line = clr.Convert(element.Curve, DB.Line)
        direction = line.Direction

    elif isinstance(element, (DB.Wall)):
        location_crv = clr.Convert(element.Location, DB.LocationCurve)

        try:
            line = clr.Convert(location_crv.Curve, DB.Line)
        except TypeError:
            logger.warning('Element not straight...')
            return

        direction = line.Direction

    elif isinstance(element, (DB.FamilyInstance)):
        direction = element.FacingOrientation

    else:
        print("Element of type {} not supported".format(type(element)))
        return

    return direction



def element_centre_point(element):
    """
    """
    if isinstance(element, (DB.Wall)):
        location_crv = clr.Convert(element.Location, DB.LocationCurve)
        centre_pt = location_crv.Curve.Evaluate(0.5, True)
    else:
        message = "Centre point for type {} not yet supported".format(
            type(element))
        # logger.debug(message)
        raise TypeError(message)
        # return

    return centre_pt


def straighten_element(element, guides, rotation_point=None, normal=DB.XYZ(0, 0, 1), doc=revit.doc):
    direction = element_direction(element)
    angles = []

    for guide in guides:
        angle = direction.AngleOnPlaneTo(guide, normal)# + math.pi / 2
        angles.append(angle)

    angle = sorted(angles, key=lambda x: abs(math.sin(x)))[0]
    rotation_angle = math.atan(math.tan(angle))  # - math.pi/2

    centre_pt = element_centre_point(element)
    axis = DB.Line.CreateUnbound(centre_pt, normal)

    # print(angle/math.pi*180.0, rotation_angle/math.pi*180.0)

    # rotation_transform = DB.Transform.CreateRotationAtPoint(normal, angle, centre_pt)
    DB.ElementTransformUtils.RotateElement(doc, element.Id, axis, rotation_angle)
    # wall.Location.Rotate(axis, rotation_angle)

    return element
