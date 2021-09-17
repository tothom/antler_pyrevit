from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms

from collections import OrderedDict
from System.Collections.Generic import List

__doc__ = "Color Elements in View by Selected Parameter"
__title__ = "Color by Parameter"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

def random_numbers(seed, count=1):
	"""
	Returns a list of random numbers from given seed. The seed can be anything: numbers, strings, class instances and so on.
	"""
	from System import Random

	rand = Random(int(hash(seed)))
	numbers = [rand.NextDouble() for _ in range(count)]

	return numbers

def brighter_color(color):
	"""
	Brighter fill pattern colour
	"""
	r = color.Red   + (255-color.Red)   / 2
	g = color.Green + (255-color.Green) / 2
	b = color.Blue  + (255-color.Blue)  / 2

	return Color(r, g, b)

def darker_color(color):
	"""

	"""
	r = color.Red   / 2
	g = color.Green / 2
	b = color.Blue  / 2

	return Color(r, g, b)


def override_element_color(element, color, view, fill_color=None, line_color=None):

	# Get solid fill pattern
	solid_fill =  FillPatternElement.GetFillPatternElementByName(doc, FillPatternTarget.Drafting, "<Solid fill>")

	#create graphic overrides properties
	graphic_settings = OverrideGraphicSettings()

	if fill_color is not None:
		fill_color = dscolor_to_rcolor(ds_fill_colors[i])

		# Sets projection overrides
		graphic_settings.SetSurfaceBackgroundPatternId(solid_fill.Id)
		graphic_settings.SetSurfaceBackgroundPatternColor(fill_color)

		# Sets cut overrides
		graphic_settings.SetCutBackgroundPatternId(solid_fill.Id)
		graphic_settings.SetCutBackgroundPatternColor(fill_color)

	if line_color is not None:
		line_color = dscolor_to_rcolor(ds_line_colors[i])
		# Sets projection overrides
		graphic_settings.SetProjectionLineColor(line_color)

		# Sets cut overrides
		graphic_settings.SetCutLineColor(line_color)

	view.SetElementOverrides(element.Id, graphic_settings)


# Select Levels
levels = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
levels_dict = {"{} ({})".format(level.Name, level.Elevation): level for level in levels}

levels_dict = OrderedDict(sorted(levels_dict.items(), key=lambda (key, value): value.Elevation, reverse=True))
level_key = forms.SelectFromList.show(levels_dict.keys(), button_name='Select Level', multiple=False, message='Select level to change to.')
level = levels_dict.get(level_key) # Using get() to avoid error message when cancelling dialog.
# levels = forms.select_levels()

elements = []

if level:
	# for level in levels:
	elements.extend(get_elements_on_level(level))

element_id_collection = List[DB.ElementId]([element.Id for element in elements])

uidoc.Selection.SetElementIds(element_id_collection)
