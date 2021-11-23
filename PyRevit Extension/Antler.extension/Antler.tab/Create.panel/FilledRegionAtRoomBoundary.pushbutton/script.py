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

filled_region_type = antler.ui.select_filled_region()

with DB.Transaction(revit.doc, __commandname__) as t:
    t.Start()

    for room in rooms:
        element = antler.instances.filled_region_from_room(filled_region_type, room)

    t.Commit()
