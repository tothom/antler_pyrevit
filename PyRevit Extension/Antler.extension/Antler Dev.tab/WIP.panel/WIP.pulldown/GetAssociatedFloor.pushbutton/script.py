# from System.Collections.Generic import *
from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

import antler
import math

from System.Collections.Generic import List

TOLERANCE = 1e-14

logger = script.get_logger()
config = script.get_config()
output = script.get_output()

# Select Elements
selection = revit.uidoc.Selection.PickObject(
    UI.Selection.ObjectType.Element, "Select Window...")

element = revit.doc.GetElement(selection)

element_id, pt = antler.geometry.find_associated_floor(element, revit.uidoc.ActiveView)

logger.info(element_id, pt)

revit.uidoc.Selection.SetElementIds(List[DB.ElementId]([element_id]))
