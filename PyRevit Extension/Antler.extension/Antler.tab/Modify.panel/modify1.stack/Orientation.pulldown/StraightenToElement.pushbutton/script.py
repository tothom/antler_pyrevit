from System.Collections.Generic import List
from rpw import revit, DB, UI

from pyrevit import forms, script, EXEC_PARAMS

import math
# import clr
import antler.transform

uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()
config = script.get_config()

def configure(config):
    global guide_ids, angle_snap

    references = uidoc.Selection.PickObjects(UI.Selection.ObjectType.Element, "Select objects to act as guides...")
    # except Autodesk.Revit.Exceptions.OperationCanceledException:
    #     script.exit()

    guide_ids = []

    for ref in references:
        if antler.transform.element_direction(doc.GetElement(ref)): # Only elements where direction can be extracted are included.
            guide_ids.append(ref.ElementId)

    if not guide_ids:
        logger.error("No valid guide elements selected")
        return

    config.guide_ids = [id.IntegerValue for id in guide_ids]

    angle_snap = forms.CommandSwitchWindow.show(
        [15, 30, 45, 60, 90],
        message='Snap angle. ESC for no additional angle snapping.'
    )

    config.angle_snap = angle_snap

    script.save_config()

# Config mode
if EXEC_PARAMS.config_mode:
    configure(config)

try:
    guide_ids = config.guide_ids
    angle_snap = config.angle_snap
except Exception as e:
    logger.debug(e)
    configure(config)



logger.debug(guide_ids)
logger.debug(angle_snap)


guides = []

for id_integer in guide_ids:
    element_id = DB.ElementId(id_integer)
    element = doc.GetElement(element_id)
    guide = antler.transform.element_direction(element)

    if guide:
        guides.append(guide)

if not angle_snap:
    angle_snap = 0

angle_snap = angle_snap / 180.0 * math.pi

axis_pt = None

# Axis of rotation settings
# if EXEC_PARAMS.debug_mode:
#     axis_pt = uidoc.Selection.PickPoint("Select axis point for rotation...")
# else:
#     axis_pt = None

# Select Elements to straighten
selection = uidoc.Selection.GetElementIds() or uidoc.Selection.PickObjects(UI.Selection.ObjectType.Element, "Select objects to straighten...")
elements = [doc.GetElement(id) for id in selection]

if guides:
    with DB.Transaction(doc, __commandname__) as t:
        t.Start()

        for element in elements:
            antler.transform.straighten_element(
                element, guides, axis_pt=axis_pt, angle_snap=angle_snap)

        t.Commit()
