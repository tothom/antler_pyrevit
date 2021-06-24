from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms

import math
import clr

uidoc = revit.uidoc
doc = revit.doc

def align_wall_direction(wall, directions):
    """
    """
    angles = []

    for direction in directions:
        angle = wall.Orientation.AngleOnPlaneTo(direction, DB.XYZ(0, 0, 1))

        angles.append(angle)

    angle = sorted(angles, key=lambda x: abs(math.sin(x)))[0]
    # print(angles, angle)

    angle = math.atan(math.tan(angle))

    wall_crv = clr.Convert(wall.Location, DB.LocationCurve)
    wall_center_pt = wall_crv.Curve.Evaluate(0.5, True)

    axis = DB.Line.CreateUnbound(wall_center_pt, DB.XYZ(0,0,1))

    # print(wall_crv)

    wall.Location.Rotate(axis, angle)

    return wall


# Select Elements
selection = uidoc.Selection.GetElementIds() or uidoc.Selection.PickObjects(
    UI.Selection.ObjectType.Element)
elements = [doc.GetElement(id) for id in selection]


with DB.Transaction(doc, __commandname__) as t:
    t.Start()

    for element in elements:
        align_wall_direction(
            element, [uidoc.ActiveView.RightDirection, uidoc.ActiveView.UpDirection])

    t.Commit()
