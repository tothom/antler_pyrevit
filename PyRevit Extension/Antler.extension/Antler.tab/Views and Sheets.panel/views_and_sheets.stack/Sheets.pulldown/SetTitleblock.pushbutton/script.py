# from System.Collections.Generic import *
from rpw import revit, DB

from pyrevit import forms, script
import antler

import sheets_util

logger = script.get_logger()


def replace_titleblock(sheet, titleblock):
    titleblocks_on_sheet = sheets_util.titleblocks_on_sheet(sheet)

    logger.debug(titleblocks_on_sheet)

    if len(titleblocks_on_sheet) == 1:
        titleblocks_on_sheet[0].Symbol = titleblock
    elif len(titleblocks_on_sheet) > 1:
        logger.warning("More than one titleblock found on sheet")
    else:
        logger.warning("No titleblocks found on sheet.")



# Select Sheets
sheets = forms.select_sheets(use_selection=True) or script.exit()

if script.CONFI


titleblock = antler.forms.select_of_category(
    DB.BuiltInCategory.OST_TitleBlocks,
    lambda x: "{} - {}".format(
        x.Family.Name,
        x.get_Parameter(DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        ),
    multiselect=False
    ) or script.exit()


logger.debug(titleblock)


with DB.Transaction(revit.doc, __commandname__) as t:
    t.Start()

    for sheet in sheets:
        replace_titleblock(sheet, titleblock)

    t.Commit()
