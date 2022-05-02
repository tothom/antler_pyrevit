from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms

from collections import OrderedDict
from System.Collections.Generic import List

__doc__ = "Uncut multiple elements with one cutter"
__title__ = "Uncut multiple"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

references = uidoc.Selection.GetElementIds() or uidoc.Selection.PickObjects(UI.Selection.ObjectType.Element, "Select elements to be uncut...")

if references:
    with DB.Transaction(doc, __title__) as t:
        t.Start()

        for reference in references:
            element = doc.GetElement(reference.ElementId)

            cutting_void_ids = DB.InstanceVoidCutUtils.GetCuttingVoidInstances(element)

            cutters = [doc.GetElement(id) for id in cutting_void_ids]

            for cutter in cutters:
                try:
                    DB.InstanceVoidCutUtils.RemoveInstanceVoidCut(doc, element, cutter)
                except Exception as e:
                    print(e)

        t.Commit()
