# -*- coding: utf-8 -*-

from rpw import revit, DB, UI

from pyrevit import forms, script, EXEC_PARAMS

import antler

logger = script.get_logger()
output = script.get_output()


class grid_filter(UI.Selection.ISelectionFilter):
    def AllowElement(self, element):
        if element.Category.Name == "Grids":
            return True
        else:
            return False

    def AllowReference(self, ref, pt):
        return True

if EXEC_PARAMS.config_mode:
    grid_refs = revit.uidoc.Selection.PickObjects(
        UI.Selection.ObjectType.Element,
        grid_filter(),
        "Select destination grids to match vertical extends")

    for ref in grid_refs:
        grid = revit.doc.GetElement(ref)
        outline = grid.GetExtents()

        print("{name}: min: {min}, max: {max}".format(
            name=grid.Name,
            min=outline.MinimumPoint,
            max=outline.MaximumPoint
        ))

else:
    source_grid_ref = revit.uidoc.Selection.PickObject(
        UI.Selection.ObjectType.Element, grid_filter(), "Select source grid")


    destination_grid_refs = revit.uidoc.Selection.PickObjects(
        UI.Selection.ObjectType.Element,
        grid_filter(),
        "Select destination grids to match vertical extends")
    # grids = antler.ui.preselect(DB.Grid)

    source_grid = revit.doc.GetElement(source_grid_ref)

    outline = source_grid.GetExtents()

    top_extent = outline.MaximumPoint.Z
    bottom_extent = outline.MinimumPoint.Z

    with DB.Transaction(revit.doc, __commandname__) as t:
        t.Start()

        for ref in destination_grid_refs:
            grid = revit.doc.GetElement(ref)
            grid.SetVerticalExtents(bottom_extent, top_extent)

        t.Commit()
