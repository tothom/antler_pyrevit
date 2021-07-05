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

def configure(config):
    # Set handing parameter
    # handing_parameter_name = "Comments"

    config.handing_parameter_name = "Comments"

try:
    pass
except:
    pass

# Get all doors and windows
collector = DB.FilteredElementCollector(doc)
doors = collector.OfCategory(DB.BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()

collector = DB.FilteredElementCollector(doc)
windows = collector.OfCategory(DB.BuiltInCategory.OST_Windows).WhereElementIsNotElementType().ToElements()

elements = list(doors) + list(windows)

# print(elements)

with DB.Transaction(doc, __commandname__) as t:
    t.Start()

    for element in elements:
        parameter = element.LookupParameter("Comments")

        if element.HandFlipped != element.FacingFlipped:
            parameter.Set("R")
        else:
            parameter.Set("L")

    t.Commit()
