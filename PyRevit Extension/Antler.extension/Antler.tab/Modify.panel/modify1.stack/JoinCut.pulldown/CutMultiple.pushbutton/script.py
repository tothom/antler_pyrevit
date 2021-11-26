from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms

from collections import OrderedDict
from System.Collections.Generic import List

__doc__ = "Cut multiple elements with one cutter"
__title__ = "Cut multiple"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc


if uidoc.Selection.GetElementIds():
    elements = [doc.GetElement(id) for id in uidoc.Selection.GetElementIds()]
else:
    references = uidoc.Selection.PickObjects(
        UI.Selection.ObjectType.Element, "Select elements to be cut...")
    elements = [doc.GetElement(reference.ElementId)
                for reference in references]

cutter_reference = uidoc.Selection.PickObject(
    UI.Selection.ObjectType.Element, "Select cutter...")
cutter = doc.GetElement(cutter_reference.ElementId)


if elements:
    with DB.Transaction(doc, __title__) as t:
        t.Start()
        for element in elements:
            try:
                DB.InstanceVoidCutUtils.AddInstanceVoidCut(
                    doc, element, cutter)
            except Exception as e:
                #print(e)
                pass
        t.Commit()
