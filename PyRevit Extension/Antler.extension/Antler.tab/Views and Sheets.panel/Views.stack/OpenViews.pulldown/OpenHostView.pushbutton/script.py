"""
"""
import antler
from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script

logger = script.get_logger()

selected_element = antler.util.preselect()[0]

if selected_element.ViewSpecific:
    host_view = revit.doc.GetElement(selected_element.OwnerViewId)
    revit.uidoc.ActiveView = host_view
else:
    logger.warning("Selected Element is not owned by a View")
