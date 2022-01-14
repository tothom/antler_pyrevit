# from System.Collections.Generic import *
from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

import antler
import math
# import clr

from System.Drawing import Color  # noqa: E402


uidoc = revit.uidoc
doc = revit.doc

TOLERANCE = 1e-14

logger = script.get_logger()
config = script.get_config()
output = script.get_output()

# Select Elements
selection = uidoc.Selection.GetElementIds() or uidoc.Selection.PickObjects(
    UI.Selection.ObjectType.Element, "Select objects to check...")

elements = [doc.GetElement(id) for id in selection]


with DB.Transaction(revit.doc, __commandname__) as t:
    t.Start()

    for element in elements:
        element_link = output.linkify(element.Id)

        print("Checking element {element}".format(element=element_link))

        direction = antler.transform.element_direction(element)

        if direction is None:
            continue

        angle_to_right = direction.AngleOnPlaneTo(
            uidoc.ActiveView.RightDirection, DB.XYZ.BasisZ)

        print("Element is oriented {angle} degrees in relation to right directon of current view".format(
            element=element_link, angle=angle_to_right / math.pi * 180.0)) % 180

        if abs(math.tan(angle_to_right)) < TOLERANCE:
            print("Element is parallel to right directon of view")
        else:
            print("Element is NOT parallel to right directon of view")


        angle_to_up = direction.AngleOnPlaneTo(
            uidoc.ActiveView.UpDirection, DB.XYZ.BasisZ)

        print("Element is oriented {angle} degrees in relation to up directon of current view".format(
            element=element_link, angle=angle_to_up / math.pi * 180.0)) % 180

        if abs(math.tan(angle_to_up)) < TOLERANCE:
            print("Element is parallel to up directon of view")
        else:
            print("Element is NOT parallel to up directon of view")

        if EXEC_PARAMS.config_mode:
            modulus = math.pi / 2.0
            hue = (angle_to_up % modulus) / modulus
            r, g, b = antler.color.hsv_to_rgb(hue, 0.8, 0.6)

            line_color = Color.FromArgb(int(r*255), int(g*255), int(b*255))

            # modulus = math.pi / 1.0
            # seed = (angle_to_up % modulus) / modulus
            # line_color = antler.color.random_hsv_color(
    		# 	seed=seed, s=0.7, v=0.7)

            fill_color = antler.color.relative_color_hsv(line_color, dv=+0.2)

            antler.view.override_element_color(
                element, uidoc.ActiveView, fill_color=fill_color, line_color=line_color)

        # print(math.tan(angle_to_right))
        # print(math.tan(angle_to_up))
    t.Commit()
