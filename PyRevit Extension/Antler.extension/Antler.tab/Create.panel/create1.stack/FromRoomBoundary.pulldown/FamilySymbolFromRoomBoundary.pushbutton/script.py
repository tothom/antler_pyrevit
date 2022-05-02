# -*- coding: utf-8 -*-

from rpw import revit, DB, UI
from rpw.exceptions import RevitExceptions
# from rpw.Exceptions import OperationCanceledException

from pyrevit import forms, script, EXEC_PARAMS

import antler

logger = script.get_logger()
output = script.get_output()

# print(dir(revit))

#
# class room_filter(UI.Selection.ISelectionFilter):
#     def AllowElement(self, element):
#         if element.Category.Name == "Rooms":
#             return True
#         else:
#             return False
#
#     def AllowReference(self, ref, pt):
#         return True


try:
    rooms = revit.uidoc.Selection.PickObjects(
        UI.Selection.ObjectType.Element, antler.filters.category_name_filter('Rooms'), "Select rooms")
except RevitExceptions.OperationCanceledException:
    script.exit()

rooms = [revit.doc.GetElement(room) for room in rooms]

family_symbol = antler.forms.select_detail_family_symbol()

with DB.Transaction(revit.doc, __commandname__) as t:
    t.Start()

    for room in rooms:
        element = antler.instances.place_at_room_boundary(family_symbol, room)

    t.Commit()
