from rpw import revit, DB, UI
from pyrevit import forms, script

logger = script.get_logger()

giant_bounding_box = DB.BoundingBoxXYZ()

dim = 10000

giant_bounding_box.set_MinEnabled( 0, True )
giant_bounding_box.set_MinEnabled( 1, True )
giant_bounding_box.set_MinEnabled( 2, True )
giant_bounding_box.Min = DB.XYZ( -dim, -dim, 0 )

giant_bounding_box.set_MaxEnabled( 0, True )
giant_bounding_box.set_MaxEnabled( 1, True )
giant_bounding_box.set_MaxEnabled( 2, True )
giant_bounding_box.Max = DB.XYZ( dim, dim, 0 )

VIEW_ATTRIBS = {
    'CropBox': giant_bounding_box,
    'CropBoxActive': True,
    'CropBoxVisible': True
}

this_sheet = revit.uidoc.ActiveGraphicalView

with DB.TransactionGroup(revit.doc, __commandname__) as tg:
    tg.Start()

    viewport_ids = this_sheet.GetAllViewports()

    assert len(viewport_ids) == 1, "Only sheets with one viewport are supported."

    this_viewport = revit.doc.GetElement(viewport_ids[0])
    this_view = revit.doc.GetElement(this_viewport.ViewId)

    other_sheets = forms.select_sheets(use_selection=True)

    with DB.Transaction(revit.doc, "Set Crop Box") as t:
        t.Start()

        this_scope_box_parameter = this_view.get_Parameter(DB.BuiltInParameter.VIEWER_VOLUME_OF_INTEREST_CROP)

        this_scope_box_id = this_scope_box_parameter.AsElementId()
        this_scope_box_parameter.Set(DB.ElementId(-1))

        this_view_attribs = {}

        for attrib, value in VIEW_ATTRIBS.items():
            this_view_attribs[attrib] = getattr(this_view, attrib)
            setattr(this_view, attrib, value)

        t.Commit()

    this_box_center = this_viewport.GetBoxCenter()

    if not other_sheets:
        script.exit()

    for other_sheet in other_sheets:
        with DB.Transaction(revit.doc, "Align Viewport") as t:
            t.Start()

            other_viewport_ids = other_sheet.GetAllViewports()

            if not len(other_viewport_ids) == 1:
                logger.warning("Only sheets with one viewport are supported. Skipping aligment of {}.".format(other_sheet.SheetNumber))

            other_viewport = revit.doc.GetElement(other_viewport_ids[0])
            other_view = revit.doc.GetElement(other_viewport.ViewId)
            other_scope_box_parameter = other_view.get_Parameter(DB.BuiltInParameter.VIEWER_VOLUME_OF_INTEREST_CROP)

            other_scope_box_id = other_scope_box_parameter.AsElementId()
            this_scope_box_parameter.Set(DB.ElementId(-1))

            other_view_attribs = {}

            for attrib, value in VIEW_ATTRIBS.items():
                other_view_attribs[attrib] = getattr(other_view, attrib)
                setattr(other_view, attrib, value)

            other_viewport.SetBoxCenter(this_box_center)

            for attrib, value in other_view_attribs.items():
                setattr(other_view, attrib, value)

            t.Commit()

    with DB.Transaction(revit.doc, "Set Scope Box") as t:
        t.Start()

        this_scope_box_parameter.Set(this_scope_box_id)

        for attrib, value in this_view_attribs.items():
            setattr(this_view, attrib, value)

        t.Commit()

    tg.Assimilate()
