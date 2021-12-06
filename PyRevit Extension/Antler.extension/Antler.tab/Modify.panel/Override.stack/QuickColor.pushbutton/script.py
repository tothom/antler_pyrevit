import antler

from rpw import revit, DB, UI
from pyrevit import forms, script

import clr
clr.AddReference("System.Drawing")

from System.Drawing import Color  # noqa: E402

logger = script.get_logger()

elements = antler.ui.preselect()

if not elements:
	script.exit()

swatch = forms.select_swatch()

logger.debug(swatch)

color = Color.FromArgb(swatch.red, swatch.green, swatch.blue)

line_color = color
fill_color = antler.color.relative_color_hsv(line_color, dv=+0.4, ds=-0.4)

logger.debug(line_color)
logger.debug(fill_color)

with DB.Transaction(revit.doc, __commandname__) as t:
	t.Start()

	for element in elements:
		antler.view.override_element_color(
				element, revit.uidoc.ActiveView, fill_color=fill_color, line_color=line_color)

	t.Commit()
