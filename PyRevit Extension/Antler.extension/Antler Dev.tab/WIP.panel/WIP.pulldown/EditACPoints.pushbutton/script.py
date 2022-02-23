"""
https://pythoncvc.net/?p=116
https://spiderinnet.typepad.com/blog/2011/04/implement-the-iselectionfilter-interface-of-revit-api.html
"""

from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms

from collections import OrderedDict
from System.Collections.Generic import List

__doc__ = "Edit multiple Adaptive Component points."
__title__ = "Edit Adaptive Components"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

class AdaptivePointSelectionFilter(UI.Selection.ISelectionFilter):

    def AllowElement(self, element):
        return False
        # return isinstance(element, DB.ReferencePoint)


    def AllowReference(self, ref, pos):
        return isinstance(ref.GeometryObject, DB.Point)
        # return True
        # print(ref)
        # return isinstance(ref, DB.ElementReferenceType.REFERENCE_TYPE_NONE)
        # return True

# references = uidoc.Selection.PickObjects(
#     UI.Selection.ObjectType.PointOnElement, "Select Adaptive Component points...")

references = uidoc.Selection.PickElementsByRectangle(AdaptivePointSelectionFilter(), "Select Adaptive Component points...")
# references = uidoc.Selection.PickObjects(UI.Selection.ObjectType.PointOnElement, AdaptivePointSelectionFilter(), "Select Adaptive Component points...")

elements = []


for reference in references:
    print(
        reference.ElementReferenceType,
        reference.ElementId,
        reference.GlobalPoint,
        reference.UVPoint
        )

    element = doc.GetElement(reference.ElementId)

    print(
        element,
        # dir(element)
        )


#
#
# if elements:
#     with DB.Transaction(doc, __title__) as t:
#         t.Start()
#         for element in elements:
#
#         t.Commit()
