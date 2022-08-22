from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script

import antler

from dataclasses import dataclass

logger = script.get_logger()



def duplicate_sheet(
        sheet,
        number=None,
        name=None,
        duplicate_option=DB.ViewDuplicateOption.WithDetailing,
        destination_doc=revit.doc):
    """
    Duplicates sheet with all Views
    """
    source_doc = sheet.Document
    # Get all Viewports and Titleblock from Sheet
    viewport_ids = sheet.GetAllViewports()
    viewports = [sheet.Document.GetElement(a) for a in viewport_ids]

    titleblocks = antler.collectors.titleblocks_on_sheet_collector(sheet).ToElements()

    titleblock = titleblocks[0] # Quick workaround

    with DB.TransactionGroup(destination_doc, __commandname__) as tg:
        tg.Start()

        with DB.Transaction(destination_doc, "Create Sheet") as t:
            t.Start()

            sheet_duplicate = DB.ViewSheet.Create(destination_doc, titleblock.GetTypeId())
            sheet_duplicate.Name = sheet.Name

            t.Commit()

        with DB.Transaction(destination_doc, "Duplicate Views and place on Sheet") as t:

            t.Start()

            for viewport in viewports:
                # viewport = doc.GetElement(viewport_id)
                # view_id = viewport.ViewId
                view = sheet.Document.GetElement(viewport.ViewId)

                logger.debug(view)
                logger.debug(type(view))

                if destination_doc != sheet.Document:
                    view_duplicate_ids = DB.ElementTransformUtils.CopyElements(
                        sheet.Document,
                        List[DB.ElementId]([view.Id]),
                        destination_doc,
                        DB.Transform.Identity,
                        DB.CopyPasteOptions()
                        )
                    viewport_duplicate = DB.Viewport.Create(
                        destination_doc, sheet_duplicate.Id, view_duplicate_ids[0], viewport.GetBoxCenter())

                elif view.ViewType in (DB.ViewType.Schedule, DB.ViewType.Legend):
                    viewport_duplicate = DB.Viewport.Create(
                        destination_doc, sheet_duplicate.Id, view.Id, viewport.GetBoxCenter())
                else:
                    view_duplicate_id = view.Duplicate(duplicate_option)
                    viewport_duplicate = DB.Viewport.Create(
                        destination_doc, sheet_duplicate.Id, view_duplicate_id, viewport.GetBoxCenter())

                # Synchronize Viewport properties
                viewport_duplicate.Rotation = viewport.Rotation

                # viewport_duplicate.Name = viewport.element.get_Parameter(DB.BuiltInParameter.SHEET_NAME)
                try:
                    viewport_duplicate.ChangeTypeId(viewport.GetTypeId())
                except Exceptions as e:
                    logger.warning(e)


            t.Commit()

        tg.Assimilate()

    return sheet_duplicate
