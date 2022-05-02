# from System.Collections.Generic import *
from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

import antler.geometry.transform
import math
# import clr

uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()
config = script.get_config()

# Angle snap settings
def configure(config):
    global angle_snap

    angle_snap = forms.CommandSwitchWindow.show(
        [15, 30, 45, 60, 90],
        message='Snap angle. ESC for no additional angle snapping.'
    )

    config.angle_snap = angle_snap

# Config mode
if EXEC_PARAMS.config_mode:
    configure(config)

try:
    angle_snap = config.angle_snap
except Exception as e:
    logger.debug(e)
    configure(config)

script.save_config()

angle_snap = angle_snap or 0
angle_snap = angle_snap / 180.0 * math.pi

axis_pt = None

# Axis of rotation settings
# if EXEC_PARAMS.debug_mode:
#     axis_pt = uidoc.Selection.PickPoint("Select axis point for rotation...")
# else:
#     axis_pt = None

# Select Elements
selection = uidoc.Selection.GetElementIds() or uidoc.Selection.PickObjects(
    UI.Selection.ObjectType.Element, "Select objects to straighten to view...")

elements = [doc.GetElement(id) for id in selection]


with DB.Transaction(doc, __commandname__) as t:
    t.Start()

    for element in elements:
        antler.geometry.transform.straighten_element(
            element, [uidoc.ActiveView.RightDirection, uidoc.ActiveView.UpDirection], axis_pt=axis_pt, angle_snap=angle_snap)

    t.Commit()
