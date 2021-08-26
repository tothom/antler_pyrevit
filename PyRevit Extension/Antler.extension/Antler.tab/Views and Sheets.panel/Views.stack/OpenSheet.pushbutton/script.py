"""
"""
from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script

from collections import OrderedDict
from System.Collections.Generic import List

logger = script.get_logger()

uidoc = revit.uidoc
doc = revit.doc

try:
    # Don't bother if view is already a sheet.
    assert not isinstance(uidoc.ActiveView, DB.ViewSheet)

    sheet_number = uidoc.ActiveView.get_Parameter(
        DB.BuiltInParameter.VIEWPORT_SHEET_NUMBER).AsString()
except Exception as e:
    logger.warning("View is not on a Sheet")
else:
    logger.info(sheet_number)

    sheets = DB.FilteredElementCollector(
        doc).OfClass(DB.ViewSheet).ToElements()

    for sheet in sheets:
        if sheet_number == sheet.SheetNumber:
            uidoc.ActiveView = sheet
            break
