from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms

from collections import OrderedDict
from System.Collections.Generic import List

__doc__ = "Align multiple adaptive components by their points to reference planes."
__title__ = "Align Adpative Points"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

def point_distance_to_plane(pt, plane):
    pass


if uidoc.Selection.GetElementIds():
    elements = [doc.GetElement(id) for id in uidoc.Selection.GetElementIds()]
else:
    references = uidoc.Selection.PickObjects(
        UI.Selection.ObjectType.Element, "Select elements to be align...")
    elements = [doc.GetElement(reference.ElementId)
                for reference in references]

cutter_reference = uidoc.Selection.PickObject(
    UI.Selection.ObjectType.Element, "Select reference planes...")
cutter = doc.GetElement(cutter_reference.ElementId)


if elements:
    with DB.Transaction(doc, __title__) as t:
        t.Start()



        # for element in elements:
            #
            # placement_point_ids = DB.AdaptiveComponentInstanceUtils.GetInstancePlacementPointElementRefIds(element)
            #
            # # Move point to plane
            #
            # doc.Create.NewAlignment(view, ref_plane, ref_point)

        t.Commit()
