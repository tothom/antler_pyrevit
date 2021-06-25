from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, EXEC_PARAMS

import antler

import math
import clr

uidoc = revit.uidoc
doc = revit.doc

# Angle snap settings
angle_snap = forms.CommandSwitchWindow.show(
    [30, 45, 90],
    message='Snap angle. ESC for no additional snapping angles.'
)

if not angle_snap:
    angle_snap = 0

angle_snap = angle_snap / 180.0 * math.pi

# Axis of rotation settings
if EXEC_PARAMS.config_mode:
    axis_pt = uidoc.Selection.PickPoint("Select axis point for rotation...")
else:
    axis_pt = None


# Select Elements
selection = uidoc.Selection.GetElementIds() or uidoc.Selection.PickObjects(
    UI.Selection.ObjectType.Element, "Select objects to straighten to view...")
elements = [doc.GetElement(id) for id in selection]



with DB.Transaction(doc, __commandname__) as t:
    t.Start()

    for element in elements:
        antler.transform.straighten_element(
            element, [uidoc.ActiveView.RightDirection, uidoc.ActiveView.UpDirection], axis_pt=axis_pt, angle_snap=angle_snap)

    t.Commit()
