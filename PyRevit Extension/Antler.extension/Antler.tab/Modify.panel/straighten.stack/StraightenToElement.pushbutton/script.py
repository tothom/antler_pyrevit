from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms

import math
import clr
import antler

uidoc = revit.uidoc
doc = revit.doc


# Select Element to straighten
guide_ref = uidoc.Selection.PickObject(
    UI.Selection.ObjectType.Element)  # TODO: Grid, Line, Wall, FamilyInstance

guide_element = doc.GetElement(guide_ref.ElementId)

try:
    # guide_crv = clr.Convert(guide_element.Location, DB.LocationCurve)

    guide_line = clr.Convert(guide_element.Curve, DB.Line)
    guide_direction = guide_line.Direction

except Exception as e:
    print(e)

# print(guide_direction)

# Select Elements
selection = uidoc.Selection.GetElementIds() or uidoc.Selection.PickObjects(
    UI.Selection.ObjectType.Element)
elements = [doc.GetElement(id) for id in selection]


with DB.Transaction(doc, __commandname__) as t:
    t.Start()

    for element in elements:
        antler.transform.align_wall_direction(
            element, [guide_direction])

    t.Commit()
