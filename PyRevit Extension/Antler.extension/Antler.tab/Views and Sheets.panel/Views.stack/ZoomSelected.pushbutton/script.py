# from System.Collections.Generic import *
from rpw import revit, DB, UI

import antler

elements = antler.util.preselect()

element_set = DB.ElementSet()
[element_set.Insert(element) for element in elements]

revit.uidoc.ShowElements(element_set)
