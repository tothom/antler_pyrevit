from System.Collections.Generic import *
from rpw import revit, DB, UI, ui

from pyrevit import forms

from System.Collections.Generic import List

__doc__ = "Moves Level without moving the hosted Elements."
__title__ = "Offset Level"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

def get_elements_on_level(level):
    """
    """
    level_filter = DB.ElementLevelFilter(level.Id)
    collector = DB.FilteredElementCollector(doc)
    elements = collector.WherePasses(level_filter).ToElements()

    return elements


if not uidoc.ActiveView.SketchPlane:
    res = forms.alert("Please set Work Plane before continuing")
else:
    # level = ui.Pick.pick_element(msg="Pick Level", multiple=False)
    reference = uidoc.Selection.PickObject(UI.Selection.ObjectType.Element)
    level = doc.GetElement(reference.ElementId)
    pick_pt = uidoc.Selection.PickPoint("Pick point to move to")

    # print(pt)

    translation = DB.XYZ(0, 0, pick_pt.Z - level.Elevation)
    reverse_translation = DB.XYZ(0, 0, level.Elevation - pick_pt.Z)

    hosted_elements = get_elements_on_level(level)
    element_id_collection = List[DB.ElementId]([e.Id for e in hosted_elements])

    with DB.Transaction(doc, __title__) as t:
        t.Start()

        # DB.ElementTransformUtils.MoveElement(doc, level.Id, translation)
        for element in hosted_elements:
            # location = element.Location
            element.Location.Move(DB.XYZ(0, 0, 10))
        # DB.ElementTransformUtils.MoveElements(doc, element_id_collection, reverse_translation)

        t.Commit()
