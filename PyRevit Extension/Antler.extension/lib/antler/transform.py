from rpw import revit, DB
from pyrevit import forms, script

import math
import clr


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


def align_wall_direction(wall, directions):
    """
    """
    angles = []

    for direction in directions:
        angle = wall.Orientation.AngleOnPlaneTo(direction, DB.XYZ(0, 0, 1))
        print(angle/math.pi*180)

        angles.append(angle)

    angle = sorted(angles, key=lambda x: abs(math.sin(x)))[0]

    # print(angle)

    rotation_angle = math.atan(math.tan(angle))# - math.pi/2

    print(angle/math.pi*180.0, rotation_angle/math.pi*180.0)

    wall_crv = clr.Convert(wall.Location, DB.LocationCurve)
    wall_center_pt = wall_crv.Curve.Evaluate(0.5, True)

    axis = DB.Line.CreateUnbound(wall_center_pt, DB.XYZ(0, 0, 1))

    # print(wall_crv)

    wall.Location.Rotate(axis, rotation_angle)

    return wall
