from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms

from collections import OrderedDict

__doc__ = "Calculate net area of windows and doors in relation to Areas."
__title__ = "Net Opening"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

# Get Area Scheme
area_schemes = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_AreaSchemes).WhereElementIsNotElementType().ToElements()
# print(area_schemes)
area_schemes_dict = {"{}".format(area_scheme.Name): area_scheme for area_scheme in area_schemes}
# print(area_schemes_dict)
area_scheme_key = forms.SelectFromList.show(area_schemes_dict.keys(), button_name='Select Area Scheme', multiple=False)

area_scheme = area_schemes_dict.get(area_scheme_key) # Using get() to avoid error message when cancelling dialog.
# print(area_scheme.Name)

"""
# Get Design Option
design_options = DB.FilteredElementCollector(doc).OfClass(DB.DesignOption).WhereElementIsNotElementType().ToElements()
# print(design_options)
design_option_dict = {"{}".format(design_option.Name): design_option for design_option in design_options}
# print(design_option_dict)
design_option_key = forms.SelectFromList.show(design_option_dict.keys(), button_name='Select Area Scheme', multiple=False)

design_option = design_option_dict.get(design_option_key) # Using get() to avoid error message when cancelling dialog.
# print(area_scheme.Name)
"""

# Collectors
primary_design_option_member_filter = DB.PrimaryDesignOptionMemberFilter()

window_collectors = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Windows).WhereElementIsNotElementType().ToElements()




doors = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()
areas = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Areas).WhereElementIsNotElementType().ToElements()
