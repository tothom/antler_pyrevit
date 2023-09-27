# -*- coding: utf-8 -*-

from rpw import revit, DB, UI
from rpw.exceptions import RevitExceptions
# from rpw.Exceptions import OperationCanceledException

from pyrevit import forms, script, EXEC_PARAMS

import antler

logger = script.get_logger()
output = script.get_output()

# print(dir(revit))

class room_filter(UI.Selection.ISelectionFilter):
    def AllowElement(self, element):
        if element.Category.Name == "Rooms":
            return True
        else:
            return False

    def AllowReference(self, ref, pt):
        return True

try:
    rooms = revit.uidoc.Selection.PickObjects(
        UI.Selection.ObjectType.Element, room_filter(), "Select rooms")
except RevitExceptions.OperationCanceledException:
    script.exit()

rooms = [revit.doc.GetElement(room) for room in rooms]

wall_type = antler.forms.select_types_of_category(categories=[DB.BuiltInCategory.OST_Walls], multiselect=False)

height_string = "100"

while True:
    prompt = "Enter wall height"

    height_string = forms.ask_for_string(
        default=height_string,
        prompt=prompt,
        title="Wall Height"
    )

    try:
        height = float(height_string) / 304.8
        break
    except:
        prompt = "Enter a valid wall height"
        continue


    

with DB.Transaction(revit.doc, __commandname__) as t:
    t.Start()

    for room in rooms:
        element = antler.instances.place_wall_at_room_boundary(wall_type, room, height=height)

    t.Commit()
