# -*- coding: utf-8 -*-

from rpw import revit, DB

from pyrevit import forms, script, EXEC_PARAMS

import antler

logger = script.get_logger()
output = script.get_output()

grids = antler.util.preselect(DB.Grid)

for grid in grids:
    outline = grid.GetExtents()

    logger.info("Min: {}, Max:{}".format(
        outline.MaximumPoint, outline.MinimumPoint))
