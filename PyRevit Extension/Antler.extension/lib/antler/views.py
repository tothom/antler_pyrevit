from rpw import revit, DB
import collectors, compare

from antler import LOGGER

from System.Collections.Generic import List

def query_view(view):
    pass


def override_element_color(element, view, fill_color=None, line_color=None):
    """
    Overrides color of element in view with input colors. The element will get
    a solid background fill in both cut and projection.

    If not color arguments are left empty, the element will get it's overrides removed.
    """
    # Get solid fill pattern
    solid_fill = DB.FillPatternElement.GetFillPatternElementByName(
        revit.doc, DB.FillPatternTarget.Drafting, "<Solid fill>")

    #create graphic overrides properties
    graphic_settings = DB.OverrideGraphicSettings()

    if fill_color is not None:
        fill_color = DB.Color(fill_color.R, fill_color.G, fill_color.B)
        # fill_color = dscolor_to_rcolor(ds_fill_colors[i])

        # Sets projection overrides
        graphic_settings.SetSurfaceBackgroundPatternId(solid_fill.Id)
        graphic_settings.SetSurfaceBackgroundPatternColor(fill_color)

        # Sets cut overrides
        graphic_settings.SetCutBackgroundPatternId(solid_fill.Id)
        graphic_settings.SetCutBackgroundPatternColor(fill_color)

    if line_color is not None:
        line_color = DB.Color(line_color.R, line_color.G, line_color.B)

        # line_color = dscolor_to_rcolor(ds_line_colors[i])
        # Sets projection overrides
        graphic_settings.SetProjectionLineColor(line_color)

        # Sets cut overrides
        graphic_settings.SetCutLineColor(line_color)

        graphic_settings.SetSurfaceForegroundPatternColor(line_color)
        graphic_settings.SetCutForegroundPatternColor(line_color)

    view.SetElementOverrides(element.Id, graphic_settings)



def duplicate_sheet(
        sheet,
        number=None,
        name=None,
        duplicate_option=DB.ViewDuplicateOption.WithDetailing,
        titleblock=None):
    """
    Duplicates sheet with all Views
    """
    doc = sheet.Document
    # Get all Viewports and Titleblock from Sheet
    viewport_ids = sheet.GetAllViewports()
    viewports = [sheet.Document.GetElement(a) for a in viewport_ids]

    titleblocks = collectors.titleblocks_on_sheet_collector(sheet).ToElements()

    titleblock = titleblock or titleblocks[0] # Quick workaround

    with DB.TransactionGroup(doc, __commandname__) as tg:
        tg.Start()

        with DB.Transaction(doc, "Duplicate Sheet") as t:
            t.Start()

            sheet_duplicate = DB.ViewSheet.Create(
                doc, titleblock.Id)
            sheet_duplicate.Name = sheet.Name

            t.Commit()

        with DB.Transaction(doc, "Duplicate Views and place on Sheet") as t:

            t.Start()

            for viewport in viewports:

                LOGGER.debug(view)
                LOGGER.debug(type(view))


                if view.ViewType in (DB.ViewType.Schedule, DB.ViewType.Legend):
                    viewport_duplicate = DB.Viewport.Create(
                        doc, sheet_duplicate.Id, viewport.ViewId, viewport.GetBoxCenter())
                else:
                    view_duplicate_id = view.Duplicate(duplicate_option)

                    viewport_duplicate = DB.Viewport.Create(
                        doc, sheet_duplicate.Id, view_duplicate_id, viewport.GetBoxCenter())

                # Synchronize Viewport properties
                viewport_duplicate.Rotation = viewport.Rotation

                # viewport_duplicate.Name = viewport.element.get_Parameter(DB.BuiltInParameter.SHEET_NAME)
                try:
                    viewport_duplicate.ChangeTypeId(viewport.GetTypeId())
                except Exceptions as e:
                    LOGGER.warning(e)


            t.Commit()

        tg.Assimilate()

    return sheet_duplicate




def pull_sheet(
        sheet,
        number=None,
        name=None,
        duplicate_option=DB.ViewDuplicateOption.WithDetailing,
        doc=revit.doc):
    """
    Duplicates sheet with all Views
    """
    source_doc = sheet.Document
    # Get all Viewports and Titleblock from Sheet
    viewport_ids = sheet.GetAllViewports()
    viewports = [sheet.Document.GetElement(a) for a in viewport_ids]

    titleblocks = collectors.titleblocks_on_sheet_collector(sheet).ToElements()

    titleblock = titleblocks[0] # Quick workaround

    with DB.TransactionGroup(destination_doc, __commandname__) as tg:
        tg.Start()

        with DB.Transaction(destination_doc, "Create Sheet") as t:
            t.Start()

            if destination_doc != sheet.Document:
                destination_titleblock_type = compare.find_similar_element(
                    titleblock.Symbol, destination_doc)

                if not destination_titleblock_type:
                    destination_titleblock_type_id = DB.ElementTransformUtils.CopyElements(
                        sheet.Document,
                        List[DB.ElementId]([titleblock.Symbol.Id]),
                        destination_doc,
                        DB.Transform.Identity,
                        DB.CopyPasteOptions()
                        )

                    t.Commit()

                    destination_titleblock_type = compare.find_similar_element(
                        titleblock.Symbol, destination_doc)


                destination_titleblock_type_id = destination_titleblock_type.Id

            else:
                destination_titleblock_type_id = titleblock.Symbol.Id

            sheet_duplicate = DB.ViewSheet.Create(
                destination_doc, destination_titleblock_type_id)
            sheet_duplicate.Name = sheet.Name

            t.Commit()

        with DB.Transaction(destination_doc, "Duplicate Views and place on Sheet") as t:

            t.Start()

            for viewport in viewports:
                # viewport = doc.GetElement(viewport_id)
                # view_id = viewport.ViewId
                #view = sheet.Document.GetElement(viewport.ViewId)

                LOGGER.debug(view)
                LOGGER.debug(type(view))

                if destination_doc != sheet.Document:
                    #with DB.Transaction(destination_doc, "Dupliceate View") as t2:
                        # t.Start()
                    view_duplicate_ids = DB.ElementTransformUtils.CopyElements(
                        sheet.Document,
                        List[DB.ElementId]([viewport.ViewId]),
                        destination_doc,
                        DB.Transform.Identity,
                        DB.CopyPasteOptions()
                        )

                    t.Commit()

                    view_duplicate = destination_doc.GetElement(view_duplicate_ids[0])

                    LOGGER.info(view_duplicate_ids)

                    viewport_duplicate = DB.Viewport.Create(
                        destination_doc, sheet_duplicate.Id, view_duplicate.Id, viewport.GetBoxCenter())

                elif view.ViewType in (DB.ViewType.Schedule, DB.ViewType.Legend):
                    viewport_duplicate = DB.Viewport.Create(
                        destination_doc, sheet_duplicate.Id, viewport.ViewId, viewport.GetBoxCenter())
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
                    LOGGER.warning(e)


            t.Commit()

        tg.Assimilate()

    return sheet_duplicate
