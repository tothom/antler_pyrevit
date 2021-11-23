# -*- coding: utf-8 -*-

from rpw import revit, DB, UI

from pyrevit import forms, script, EXEC_PARAMS

import antler

logger = script.get_logger()
output = script.get_output()


class room_filter(UI.Selection.ISelectionFilter):
    def AllowElement(self, element):
        if element.Category.Name == "Rooms":
            return True
        else:
            return False

    def AllowReference(self, ref, pt):
        return True


rooms = revit.uidoc.Selection.PickObjects(
    UI.Selection.ObjectType.Element, room_filter(), "Select rooms")

rooms = [revit.doc.GetElement(room) for room in rooms]

family_symbol = antler.ui.select_detail_family_symbol()

with DB.Transaction(revit.doc, __commandname__) as t:
    t.Start()

    for room in rooms:
        element = antler.instances.place_at_room_boundary(family_symbol, room)

    t.Commit()
