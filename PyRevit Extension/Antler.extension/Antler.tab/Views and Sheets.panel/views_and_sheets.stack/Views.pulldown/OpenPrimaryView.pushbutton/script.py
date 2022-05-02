"""
"""
from rpw import revit
from pyrevit import forms

primary_view_id = revit.uidoc.ActiveView.GetPrimaryViewId()

primary_view = revit.doc.GetElement(primary_view_id)

if primary_view:
    revit.uidoc.ActiveView = primary_view
else:
    forms.alert("No primary view found. Maybe the view is not dependent?")
