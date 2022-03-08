from rpw import revit, DB
from pyrevit import forms, script

import antler.util
import math
import clr

logger = script.get_logger()
output = script.get_output()

grids = DB.FilteredElementCollector(revit.doc).OfCategory(
    DB.BuiltInCategory.OST_Grids).WhereElementIsNotElementType().ToElements()

data = []

for grid in grids:

    logger.info(isinstance(grid.Curve, DB.Line))
    try:
        line = clr.Convert(grid.Curve, DB.Line)
        direction = line.Direction

        orientation = DB.XYZ(0,1,0).AngleOnPlaneTo(direction, DB.XYZ(0,0,1))

        angle = orientation % math.pi/2.0

        angle_formatted = DB.UnitFormatUtils.Format(
            revit.doc.GetUnits(), DB.UnitType.UT_Angle, angle, True, False)
    except:
        angle_formatted = "-"

    data.append({
        'Grid Name': grid.Name,
        'Angle': angle_formatted
    })


antler.util.print_dict_list(data, title="Grid Summary")
