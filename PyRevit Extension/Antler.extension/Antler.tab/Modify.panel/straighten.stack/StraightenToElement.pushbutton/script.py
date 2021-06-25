from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script, EXEC_PARAMS

import math
import clr
import antler

uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()

# Select elements to work as direction guides
selection = uidoc.Selection.GetElementIds() or uidoc.Selection.PickObjects(
    UI.Selection.ObjectType.Element, "Select objects to act as guides...")

guide_elements = [doc.GetElement(id) for id in selection]
guides = [antler.transform.element_direction(a) for a in guide_elements]

guides = [a for a in guides if a] # To remove None values


angle_snap = forms.CommandSwitchWindow.show(
    [30, 45, 90],
    message='Snap angle. ESC for no additional snapping angles.'
)

if not angle_snap:
    angle_snap = 0

angle_snap = angle_snap / 180.0 * math.pi


if EXEC_PARAMS.config_mode:
    axis_pt = uidoc.Selection.PickPoint("Select axis point for rotation...")
else:
    axis_pt = None

# Select Elements to straighten
selection = uidoc.Selection.PickObjects(UI.Selection.ObjectType.Element, "Select objects to straighten...")
elements = [doc.GetElement(id) for id in selection]

if guides:
    with DB.Transaction(doc, __commandname__) as t:
        t.Start()

        for element in elements:
            antler.transform.straighten_element(
                element, guides, axis_pt=axis_pt, angle_snap=angle_snap)

        t.Commit()
