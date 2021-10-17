from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms

from collections import OrderedDict

__doc__ = "Changes Level of selected Elements."
__title__ = "Change Level"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

def calc_new_offset(offset, level_ex, level_new):
    elevation_diff = level_ex.Elevation - level_new.Elevation
    offset_new = elevation_diff + offset

    return offset_new

def room_change_level(room, level=None):
    """
    WIP
    Changes location level of room. Center point will remain the same.
    """
    print(room.Location)

    # for item in room:
    #     print(item)

    return

    room.Unplace()

    # plan_curcuit = DB.
    room_new = doc.NewRoom(room, plan_curcuit)


def floor_change_level(element, level_new):
    """
    Changes Level of Floor to new Level without moving the Floor.
    """
    level_param = element.get_Parameter(DB.BuiltInParameter.LEVEL_PARAM)
    offset_param = element.get_Parameter(DB.BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM)

    level_ex = doc.GetElement(element.LevelId)

    offset_new = calc_new_offset(offset_param.AsDouble(), level_ex, level_new)

    level_param.Set(level_new.Id)
    offset_param.Set(offset_new)

    return element

def roof_change_level(element, level_new):
    """
    Changes Level of Roof to new Level without moving the Roof.
    """
    level_param = element.get_Parameter(DB.BuiltInParameter.ROOF_CONSTRAINT_LEVEL_PARAM)
    offset_param = element.get_Parameter(DB.BuiltInParameter.ROOF_CONSTRAINT_OFFSET_PARAM)

    level_ex = doc.GetElement(level_param.AsElementId())

    offset_new = calc_new_offset(offset_param.AsDouble(), level_ex, level_new)

    level_param.Set(level_new.Id)
    offset_param.Set(offset_new)

    return element



def wall_change_level(element, base_level_new, top_level_new=None):
    """
    Changes Level of Wall to new Level without moving the Wall. Only changes the Base Constraint.
    """
    base_level_param = element.get_Parameter(DB.BuiltInParameter.WALL_BASE_CONSTRAINT)
    base_offset_param = element.get_Parameter(DB.BuiltInParameter.WALL_BASE_OFFSET)

    base_level_ex = doc.GetElement(base_level_param.AsElementId())
    base_offset_new = calc_new_offset(base_offset_param.AsDouble(), base_level_ex, base_level_new)

    base_level_param.Set(base_level_new.Id)
    base_offset_param.Set(base_offset_new)

    if top_level_new:
        top_level_param = element.get_Parameter(DB.BuiltInParameter.WALL_TOP_CONSTRAINT)
        top_offset_param = element.get_Parameter(DB.BuiltInParameter.WALL_TOP_OFFSET)

        top_level_ex = doc.GetElement(top_level_param.AsElementId())
        top_offset_new = calc_new_offset(top_offset_param.AsDouble(), top_level_ex, top_level_new)

        top_level_param.Set(top_level_new.Id)
        top_offset_param.Set(top_offset_new)

    return element

def element_change_level(element, level_new, level_builtin, offset_builtin):
    """
    Changes Level of Roof to new Level without moving the Roof.
    """
    level_param = element.get_Parameter(level_builtin) # DB.BuiltInParameter.ROOF_CONSTRAINT_LEVEL_PARAM
    offset_param = element.get_Parameter(offset_builtin) # DB.BuiltInParameter.ROOF_CONSTRAINT_OFFSET_PARAM

    level_ex = doc.GetElement(level_param.AsElementId())

    offset_new = calc_new_offset(offset_param.AsDouble(), level_ex, level_new)

    level_param.Set(level_new.Id)
    offset_param.Set(offset_new)

    return element

function_mapping = {
    DB.Floor:   floor_change_level,
    DB.ExtrusionRoof:   roof_change_level,
    DB.Wall:   wall_change_level,
    }

builtin_parameter_mapping = {
    DB.Floor:   (DB.BuiltInParameter.LEVEL_PARAM, DB.BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM),
    DB.ExtrusionRoof:   (DB.BuiltInParameter.ROOF_CONSTRAINT_LEVEL_PARAM, DB.BuiltInParameter.ROOF_CONSTRAINT_OFFSET_PARAM),
    DB.Wall:   (DB.BuiltInParameter.WALL_BASE_CONSTRAINT, DB.BuiltInParameter.WALL_BASE_OFFSET),
    DB.Wall:   (DB.BuiltInParameter.WALL_TOP_CONSTRAINT, DB.BuiltInParameter.WALL_TOP_OFFSET),
    }

def category_not_supported(element, level):
    print("{} not yet supported".format(type(element)))
    return None


# Select Elements
selection = uidoc.Selection.GetElementIds() or uidoc.Selection.PickObjects(UI.Selection.ObjectType.Element)
elements = [doc.GetElement(id) for id in selection]


# Select level
# levels = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
# levels_dict = {"{} ({})".format(level.Name, level.Elevation): level for level in levels}
#
# levels_dict = OrderedDict(sorted(levels_dict.items(), key=lambda (key, value): value.Elevation, reverse=True))
# level_key = forms.SelectFromList.show(levels_dict.keys(), button_name='Select Level', multiple=False, message='Select level to change to.')
# level = levels_dict.get(level_key) # Using get() to avoid error message when cancelling dialog.


levels = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
levels_dict = {"{}".format(level.Name): level for level in levels}

level_mapping_dict = {
    "A 01 Adkomst":   "B 01 Adkomst",
    "B 01 Adkomst":   "B 01 Adkomst",
    "B U1 Teknisk etg":   "B U1 Teknisk etg",
    "A U1 Teknisk etg":   "B U1 Teknisk etg",
    "A U2 Teknisk etg":   "B U2 Adkomsthall",
    "B U2 Adkomsthall":   "B U2 Adkomsthall",
    "A U3 Teknisk etg":   "B U3 Teknisk etg",
    "B U3 Teknisk etg":   "B U3 Teknisk etg",
    "Oppdragets nullpunkt":   "Oppdragets nullpunkt",
    "A U4 Teknisk etg":   "B U4 Teknisk etg",
    "B U4 Teknisk etg":   "B U4 Teknisk etg",
    "A U5 Plattform":   "B U5 Plattform",
    "B U5 Plattform":   "B U5 Plattform",
    "Spor":   "Spor",
    "U6":   "U6"
    }



if elements and level:
    with DB.Transaction(doc, __title__) as t:
        t.Start()

        for element in elements:
            # print(element)
            function = function_mapping.get(type(element), category_not_supported)

            function(element, level)

        t.Commit()

import os
log_path = os.path.join(__commandpath__, 'test.log')
# print(log_path)

with open(log_path, 'w') as f:
    f.write('Hello World!')
