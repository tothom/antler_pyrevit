"""
It seems that changing element host through the API is not possible.
"""

# from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script
# from collections import OrderedDict

# import antler

logger = script.get_logger()


# Select Elements
selection = revit.uidoc.Selection.GetElementIds() or uidoc.Selection.PickObjects(
    UI.Selection.ObjectType.Element)

elements = [revit.doc.GetElement(id) for id in selection]

if elements:
    with DB.Transaction(revit.doc, __commandname__) as t:
        t.Start()

        for element in elements:
            try:
                level_id = element.get_Parameter(
                    DB.BuiltInParameter.FAMILY_LEVEL_PARAM).AsElementId()

                # host_parameter = element.get_Parameter(
                #     DB.BuiltInParameter.HOST_ID_PARAM)
                #
                # host_parameter.Set(level_id)

                element.HostId = level_id

            except Exception as e:
                logger.warning(e)

        t.Commit()
