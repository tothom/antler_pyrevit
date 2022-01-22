from System.Collections.Generic import *
from rpw import revit, DB, UI

__doc__ = "Measure height between to Elements "
__title__ = "Measure Height"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

with DB.Transaction(doc, __title__) as t:
    t.Start()

    pass

    t.Commit()
