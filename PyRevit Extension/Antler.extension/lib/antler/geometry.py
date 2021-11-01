from rpw import revit, DB
from pyrevit import forms, script

import math
import clr
import util

logger = script.get_logger()


def mesh_from_floor(floor, **mesh_settings):
    floor_curve_loops = None


def analysis_mesh_from_curveloop(curve_loops, height_offset, **mesh_settings):
    material = None
    operation_result = DB.TessellatedShapeBuilder.CreateMeshByExtrusion(
        curve_loops, DB.XYZ(0, 0, 1), height_offset, material)
