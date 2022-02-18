import antler

from rpw import revit, DB
from pyrevit import forms, script, EXEC_PARAMS
from pyrevit.coreutils import colors

import clr
clr.AddReference("System.Drawing")

from System.Drawing import Color  # noqa: E402

logger = script.get_logger()
config = script.get_config()

elements = antler.ui.preselect()

if not elements:
	script.exit()

if EXEC_PARAMS.config_mode or not config.has_option('swatch_name'):
	swatch = forms.select_swatch() or script.exit()
	# if swatch:
	config.set_option('swatch_name', swatch.name)
	script.save_config()
else:
	swatch_name = config.get_option('swatch_name')
	swatch = colors.COLORS[swatch_name]



# swatch = forms.select_swatch()

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
