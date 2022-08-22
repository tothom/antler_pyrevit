from System.Collections.Generic import List
from rpw import revit, DB, UI

from pyrevit import forms, script, EXEC_PARAMS

import math
# import clr
import antler

uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()
config = script.get_config()

# units = doc.GetUnits()
# print(units)

def scale_filled_region(filled_region, factor, origin=DB.XYZ(0,0,0)):
    pass

# Select Elements to straighten
selection = uidoc.Selection.GetElementIds() or uidoc.Selection.PickObjects(
    UI.Selection.ObjectType.Element, "Select Filled Regions to scale.")

elements = [doc.GetElement(a) for a in selection]



while True:
    factor = forms.ask_for_string(
        message="Scale factor")
    if factor is None:
        script.exit()
    else:
        try:
            factor = float(factor)
            break
        except ValueError:
            pass
    break

logger.info(factor)

script.exit()

transform = DB.Transform.Identity
transform.ScaleBasis = factor

# if guides:
with DB.Transaction(doc, __commandname__) as t:
    t.Start()

    for element in elements:
        result = DB.ElementTransformUtils.MoveElement(
            doc, element.Id, factor)

    t.Commit()
