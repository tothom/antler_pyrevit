from System.Collections.Generic import List
from rpw import revit, DB, UI

from pyrevit import forms, script, EXEC_PARAMS

import math
# import clr
import antler.transform

uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()
config = script.get_config()

units = doc.GetUnits()
print(units)

# Select Elements to straighten
selection = uidoc.Selection.PickObject(UI.Selection.ObjectType.Element, "Select object to translate.")
element = doc.GetElement(selection)

coordinates = forms.ask_for_string(message="Provide comma-separated coordinates...")
coordinates = [float(a)/304.8 for a in coordinates.split(',')]
translation_vector = DB.XYZ(coordinates[0], coordinates[1], 0)



# transform = DB.Transform.CreateTranslation()

# if guides:
with DB.Transaction(doc, __commandname__) as t:
    t.Start()

    result = DB.ElementTransformUtils.MoveElement(doc, element.Id, translation_vector)

    t.Commit()
