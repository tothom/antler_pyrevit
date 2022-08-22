"""
"""
from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script

import antler.forms

logger = script.get_logger()


def place_view(view, sheet):
    """
    Cannot post command with arguments, so this doesn't work.
    """
    try:
        command_id = RevitCommandId.LookupPostableCommandId(PostableCommand.PlaceAComponent);

        if command_id:
            revit.uiapp.PostCommand(command_id)

    except Exception as e:
        logger.warning(e)


# Don't bother if view is already a sheet.
assert not isinstance(revit.uidoc.ActiveView, DB.ViewSheet)

sheet_number_parameter = revit.uidoc.ActiveView.get_Parameter(
    DB.BuiltInParameter.VIEWPORT_SHEET_NUhMBER)

assert not sheet_number_parameter.HasValue

sheets = []

for ui_view in revit.uidoc.GetOpenUIViews():
    view = revit.doc.GetElement(ui_view.ViewId)

    logger.debug([view, view.Title])

    if isinstance(view, DB.ViewSheet):
        sheets.append(view)

if len(sheets) == 1:
    sheet = sheets[0]
elif len(sheets) > 1:
    # sheet = forms.select_sheets(use_selection=False, Multiselect=False)
    sheet = antler.forms.select_elements(
        sheets,
        naming_function=lambda x:"{number} - {name}".format(number=x.SheetNumber, name=x.Name),
        multiselect=False) or script.exit()
else:
    script.exit()


revit.uidoc.ActiveView = sheet

revit.uidoc.PromptToPlaceViewOnSheet(revit.uidoc.ActiveView, False)
