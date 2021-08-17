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
output = script.get_output()

# Select Elements
selection = uidoc.Selection.GetElementIds() or uidoc.Selection.PickObjects(
    UI.Selection.ObjectType.Element, "Select objects to check...")

elements = [doc.GetElement(id) for id in selection]

for element in elements:
    element_link = output.linkify(element.Id)
    print("Checking element {element}".format(element=element_link))

    direction = antler.transform.element_direction(element)


    angle_to_right = direction.AngleOnPlaneTo(
        uidoc.ActiveView.RightDirection, DB.XYZ.BasisZ)

    print("Element is oriented {angle} degrees in relation to right directon of current view".format(
        element=element_link, angle=angle_to_right / math.pi * 180.0))

    if abs(math.tan(angle_to_right)) < 1e-14:
        print("Element is parallel to right directon of view")
    else:
        print("Element is NOT parallel to right directon of view")


    angle_to_up = direction.AngleOnPlaneTo(
        uidoc.ActiveView.UpDirection, DB.XYZ.BasisZ)

    print("Element is oriented {angle} degrees in relation to up directon of current view".format(
        element=element_link, angle=angle_to_up / math.pi * 180.0))

    if abs(math.tan(angle_to_up)) < 1e-14:
        print("Element is parallel to up directon of view")
    else:
        print("Element is NOT parallel to up directon of view")

    # print(math.tan(angle_to_right))
    # print(math.tan(angle_to_up))
