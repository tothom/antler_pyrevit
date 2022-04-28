"""
"""
from rpw import revit, DB
from pyrevit import forms, script
import antler

logger = script.get_logger()

selected_element = antler.ui.preselect()[0]

if selected_element.ViewSpecific:
    host_view = revit.doc.GetElement(selected_element.OwnerViewId)
    revit.uidoc.ActiveView = host_view

    element_set = DB.ElementSet()
    element_set.Insert(selected_element)
    revit.uidoc.ShowElements(element_set)
else:
    logger.warning("Selected Element is not owned by a View")
