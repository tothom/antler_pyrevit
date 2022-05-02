"""
"""

from rpw import revit, DB
from pyrevit import forms, script

logger = script.get_logger()

uidoc = revit.uidoc
doc = revit.doc

try:
    # Don't bother if view is already a sheet.
    assert not isinstance(uidoc.ActiveView, DB.ViewSheet)

    sheet_number_parameter = uidoc.ActiveView.get_Parameter(
        DB.BuiltInParameter.VIEWPORT_SHEET_NUMBER)

    assert sheet_number_parameter.HasValue

    sheet_number = sheet_number_parameter.AsString()

    logger.debug("Sheet Number: {}".format(sheet_number))

except Exception as e:
    logger.warning("View is not on a Sheet")
else:
    sheets = DB.FilteredElementCollector(
        doc).OfClass(DB.ViewSheet).ToElements()

    for sheet in sheets:
        if sheet_number == sheet.SheetNumber:
            uidoc.ActiveView = sheet
            break
