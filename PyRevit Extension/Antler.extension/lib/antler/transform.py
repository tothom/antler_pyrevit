from rpw import revit, DB
from pyrevit import forms, script

import math

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
