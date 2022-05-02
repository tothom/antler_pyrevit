from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script

import antler

logger = script.get_logger()



def duplicate_sheet(sheet, number=None, name=None, duplicate_option=DB.ViewDuplicateOption.WithDetailing, doc=revit.doc):
    """
    Duplicates sheet with all Views
    """
    # Get all Viewports and Titleblock from Sheet
    viewport_ids = sheet.GetAllViewports()

    titleblocks = antler.collectors.titleblocks_on_sheet_collector(sheet).ToElements()

    titleblock = titleblocks[0] # Quick workaround

    with DB.TransactionGroup(revit.doc, __commandname__) as tg:
        tg.Start()

        with DB.Transaction(doc, "Create Sheet") as t:
            t.Start()

            sheet_duplicate = DB.ViewSheet.Create(doc, titleblock.GetTypeId())
            sheet_duplicate.Name = sheet.Name

            t.Commit()

        with DB.Transaction(doc, "Duplicate Views and place on Sheet") as t:

            t.Start()

            for viewport_id in viewport_ids:
                viewport = doc.GetElement(viewport_id)
                view_id = viewport.ViewId
                view = doc.GetElement(view_id)

                logger.debug(view)
                logger.debug(type(view))

                if view.ViewType in (DB.ViewType.Schedule, DB.ViewType.Legend):
                    viewport_duplicate = DB.Viewport.Create(doc, sheet_duplicate.Id, view.Id, viewport.GetBoxCenter())
                else:
                    view_duplicate_id = view.Duplicate(duplicate_option)
                    viewport_duplicate = DB.Viewport.Create(doc, sheet_duplicate.Id, view_duplicate_id, viewport.GetBoxCenter())

                # Synchronize Viewport properties
                viewport_duplicate.Rotation = viewport.Rotation

                # viewport_duplicate.Name = viewport.element.get_Parameter(DB.BuiltInParameter.SHEET_NAME)

                viewport_duplicate.ChangeTypeId(viewport.GetTypeId())

            t.Commit()

        tg.Assimilate()

    return sheet_duplicate
