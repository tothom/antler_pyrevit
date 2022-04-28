# from System.Collections.Generic import List
from rpw import revit, DB, UI

from pyrevit import forms, script, EXEC_PARAMS

# import math
# import clr
import antler

uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()
config = script.get_config()


if EXEC_PARAMS.config_mode:
    pass

source_ref = uidoc.Selection.PickObject(
    UI.Selection.ObjectType.Element, "Select SOURCE Element...")

source = revit.doc.GetElement(source_ref)

destination_ref = uidoc.Selection.PickObject(
    UI.Selection.ObjectType.Element, "Select DESTINATION Element...")

destination = revit.doc.GetElement(destination_ref)


parameters = antler.compare.diff_elements(source, destination)
# elements = [doc.GetElement(id) for id in selection]

# with DB.Transaction(revit.doc, __commandname__) as tg:
#     tg.Start()
#
#     for parameter, value in parameters.items():
#         if not parameter.IsReadOnly:
#             antler.parameters.set_parameter_value(parameter, value)
#         else:
#             logger.debug("Parameter {} is read only".format(
#                 parameter.Definition.Name))
#
#     tg.Commit()
