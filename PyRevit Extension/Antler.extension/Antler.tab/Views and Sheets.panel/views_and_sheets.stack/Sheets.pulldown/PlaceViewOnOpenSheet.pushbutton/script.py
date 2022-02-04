"""
"""
from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script

import antler.forms

logger = script.get_logger()



# try:
# Don't bother if view is already a sheet.
assert not isinstance(revit.uidoc.ActiveView, DB.ViewSheet)

sheet_number_parameter = revit.uidoc.ActiveView.get_Parameter(
    DB.BuiltInParameter.VIEWPORT_SHEET_NUMBER)

assert not sheet_number_parameter.HasValue

sheets = []

for ui_view in revit.uidoc.GetOpenUIViews():
    view = revit.doc.GetElement(ui_view.ViewId)

    logger.info([view, view.Title])

    if isinstance(view, DB.ViewSheet):
        sheets.append(view)


# sheet = forms.select_sheets(use_selection=False, Multiselect=False)
sheet = antler.forms.select_elements(
    sheets,
    naming_function=lambda x:"{number} - {name}".format(number=x.SheetNumber, name=x.Name),
    multiselect=False)

with DB.Transaction(revit.doc, __commandname__) as tg:

    try:
        tg.Start()
        viewport = DB.Viewport.Create(revit.doc, sheet.Id, revit.doc.ActiveView.Id, DB.XYZ(0,0,0))
        tg.Commit()
    except Exception as e:
        logger.warning(e)
    else:
        revit.uidoc.ActiveView = sheet
