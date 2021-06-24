from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script

import math
import clr
import antler

uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()

# Select elements to work as direction guides
selection = uidoc.Selection.GetElementIds() or uidoc.Selection.PickObjects(
    UI.Selection.ObjectType.Element)

guide_elements = [doc.GetElement(id) for id in selection]
guides = [antler.transform.element_direction(a) for a in guide_elements]

guides = [a for a in guides if a] # To remove None values

additional_rotation = forms.CommandSwitchWindow.show(
    [30, 45, 90],
    message='Additional rotations?'
)

# print(additional_rotation)

if not additional_rotation:
    additional_rotation = 0

# Select Elements to straighten
selection = uidoc.Selection.PickObjects(UI.Selection.ObjectType.Element)
elements = [doc.GetElement(id) for id in selection]

if guides:
    with DB.Transaction(doc, __commandname__) as t:
        t.Start()

        for element in elements:
            antler.transform.straighten_element(
                element, guides, angle_addition=additional_rotation/180*math.pi)

        t.Commit()
