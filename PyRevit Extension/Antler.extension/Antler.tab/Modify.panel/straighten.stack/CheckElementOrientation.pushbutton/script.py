# from System.Collections.Generic import *
from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

import antler.transform
import math
# import clr

uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()
config = script.get_config()

# Select Elements
selection = uidoc.Selection.GetElementIds() or uidoc.Selection.PickObjects(
    UI.Selection.ObjectType.Element, "Select objects to check...")

elements = [doc.GetElement(id) for id in selection]

for element in elements:
    direction = antler.transform.element_direction(element)

    angle = direction.AngleOnPlaneTo(
        uidoc.ActiveView.RightDirection, DB.XYZ.BasisZ)

    print("Element {element} is oriented {angle} degrees in relation to right directon of current view".format(
        element=element, angle=angle / math.pi * 180.0))
