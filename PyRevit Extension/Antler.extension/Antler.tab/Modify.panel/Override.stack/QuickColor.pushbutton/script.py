import antler
from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script

from collections import OrderedDict
from System.Collections.Generic import List

import clr
clr.AddReference("System.Drawing")

from System.Drawing import Color  # noqa: E402


logger = script.get_logger()

elements = antler.util.preselect()

if not elements:
	script.exit()

swatch = forms.select_swatch()

logger.debug(swatch)


color = Color.FromArgb(swatch.red, swatch.green, swatch.blue)

# script.exit()

line_color = color
fill_color = antler.color.relative_color_hsv(line_color, dv=+0.4, ds=-0.4)

logger.debug(line_color)
logger.debug(fill_color)

view = revit.uidoc.ActiveView


with DB.Transaction(revit.doc, __commandname__) as t:
	t.Start()

	for element in elements:
		antler.view.override_element_color(
				element, view, fill_color=fill_color, line_color=line_color)

	t.Commit()
