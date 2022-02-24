# from System.Collections.Generic import List
from rpw import revit, DB
from pyrevit import script, EXEC_PARAMS

import math
import antler
import clr

uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()
# config = script.get_config()

# units = doc.GetUnits()
# print(units)

def report_element_location(element):
    try:
        location = clr.Convert(element.Location, DB.LocationPoint)
        logger.info("{element} located at {x}, {y} ,{z}".format(
            element=element,
            x=float(location.Point.X)*304.8,
            y=float(location.Point.Y)*304.8,
            z=float(location.Point.Z)*304.8,
            )
        )

        return
    except Exception as e:
        logger.warning("Location for type {} not yet supported".format(type(element)))
        logger.warning(e)

selection = uidoc.Selection.GetElementIds() or uidoc.Selection.PickObjects(
    UI.Selection.ObjectType.Element, "Select objects.")

elements = [doc.GetElement(a) for a in selection]

for element in elements:
    report_element_location(element)
