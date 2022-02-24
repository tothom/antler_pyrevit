from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms

__doc__ = "Place Family Instance at Coordinates."
__title__ = "Place at Coordinates"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc


# Origin
origin = DB.XYZ(0, 0, 0)

# Project Base Point
"""
siteCategoryfilter = DB.ElementCategoryFilter(BuiltInCategory.OST_ProjectBasePoint)

collector = FilteredElementCollector(doc)
siteElements = collector.WherePasses(siteCategoryfilter).ToElements()

for ele in siteElements:

    paramX = ele.ParametersMap.get_Item("E/W")
    X = paramX.AsDouble()

    paramY = ele.ParametersMap.get_Item("N/S")
    double Y = paramY.AsDouble()

    paramElev = ele.ParametersMap.get_Item("Elev")
    double Elev = paramElev.AsDouble()

    projectBasePoint = XYZ(X, Y, Elev)
"""

# Shared sites

# shared_site = uidoc.get_Parameter(DB.BuiltInParameter.GEO_LOCATION)
shared_site = doc.ActiveProjectLocation
project_locations = doc.ProjectLocations

print([a for a in project_locations])
project_position = shared_site.GetProjectPosition(origin)

print(project_position.EastWest*304.8, project_position.NorthSouth*304.8, project_position.Elevation*304.8, project_position.Angle)

# Select Family Instance
"""
forms.SelectFromList.show(
        {'All': '1 2 3 4 5 6 7 8 9 0'.split(),
         'Odd': '1 3 5 7 9'.split(),
         'Even': '2 4 6 8 0'.split()},
        title='MultiGroup List',
        group_selector_title='Select Integer Range:',
        multiselect=True
    )
"""

# Add origin lines to Document
# with DB.Transaction(doc, __title__) as t:
#     t.Start()
#
#     if doc.IsFamilyDocument:
#
#     else:
#
#     t.Commit()

# Zoom to fit new origin elements
# element_set = DB.ElementSet()
# element_set.Insert(element_horisontal)
#
# uidoc.ShowElements(element_set)
