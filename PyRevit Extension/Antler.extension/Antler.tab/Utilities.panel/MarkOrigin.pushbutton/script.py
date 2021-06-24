from System.Collections.Generic import *
from rpw import revit, DB, UI

__doc__ = "Creates two lines in x and y direction from origin."
__title__ = "Mark Origin"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

# Prepare origin line geometry
dim = 1

origin = DB.XYZ(0, 0, 0)
xyz_x  = DB.XYZ(dim, 0, 0)
xyz_y  = DB.XYZ(0, dim, 0)

line_horisontal = DB.Line.CreateBound(origin, xyz_x)
line_vertical = DB.Line.CreateBound(origin, xyz_y)

# Add origin lines to Document
with DB.Transaction(doc, __title__) as t:
    t.Start()

    if doc.IsFamilyDocument:
        element_horisontal = doc.FamilyCreate.NewDetailCurve(uidoc.ActiveView, line_horisontal)
        element_vertical = doc.FamilyCreate.NewDetailCurve(uidoc.ActiveView, line_vertical)
    else:
        element_horisontal = doc.Create.NewDetailCurve(uidoc.ActiveView, line_horisontal)
        element_vertical = doc.Create.NewDetailCurve(uidoc.ActiveView, line_vertical)

    t.Commit()

# Zoom to fit new origin elements
element_set = DB.ElementSet()
element_set.Insert(element_horisontal)
element_set.Insert(element_vertical)

uidoc.ShowElements(element_set)
