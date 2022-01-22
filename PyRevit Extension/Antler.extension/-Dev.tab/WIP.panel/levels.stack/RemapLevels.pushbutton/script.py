from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms
from collections import OrderedDict

__doc__ = "Remap Level of selected Elements without moving them by dictionary, which is hard coded in script"
__title__ = "Remap Levels"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc


def element_change_level(element, level_new, level_builtin, offset_builtin):
    """
    Changes Level of Roof to new Level without moving the Roof.
    """
    level_param = element.get_Parameter(level_builtin) # DB.BuiltInParameter.ROOF_CONSTRAINT_LEVEL_PARAM
    offset_param = element.get_Parameter(offset_builtin) # DB.BuiltInParameter.ROOF_CONSTRAINT_OFFSET_PARAM

    level_ex = doc.GetElement(level_param.AsElementId())

    elevation_diff = level_ex.Elevation - level_new.Elevation
    offset_new = elevation_diff + offset_param.AsDouble()

    level_param.Set(level_new.Id)
    offset_param.Set(offset_new)

    return element


builtin_parameter_mapping = {
    DB.Floor:                   (DB.BuiltInParameter.LEVEL_PARAM, DB.BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM),
    DB.ExtrusionRoof:           (DB.BuiltInParameter.ROOF_CONSTRAINT_LEVEL_PARAM, DB.BuiltInParameter.ROOF_CONSTRAINT_OFFSET_PARAM),
    DB.FootPrintRoof:           (DB.BuiltInParameter.ROOF_BASE_LEVEL_PARAM, DB.BuiltInParameter.ROOF_LEVEL_OFFSET_PARAM),
    DB.FamilyInstance:          (DB.BuiltInParameter.FAMILY_LEVEL_PARAM, DB.BuiltInParameter.INSTANCE_SILL_HEIGHT_PARAM),
    DB.Ceiling:                 (DB.BuiltInParameter.LEVEL_PARAM, DB.BuiltInParameter.CEILING_HEIGHTABOVELEVEL_PARAM),
    DB.Group:                   (DB.BuiltInParameter.GROUP_LEVEL, DB.BuiltInParameter.GROUP_OFFSET_FROM_LEVEL),
    DB.Wall:                    [
                                (DB.BuiltInParameter.WALL_BASE_CONSTRAINT, DB.BuiltInParameter.WALL_BASE_OFFSET),
                                (DB.BuiltInParameter.WALL_HEIGHT_TYPE, DB.BuiltInParameter.WALL_TOP_OFFSET)
                                ],
    DB.Opening:                 [
                                (DB.BuiltInParameter.WALL_BASE_CONSTRAINT, DB.BuiltInParameter.WALL_BASE_OFFSET),
                                (DB.BuiltInParameter.WALL_HEIGHT_TYPE, DB.BuiltInParameter.WALL_TOP_OFFSET)
                                ],
    DB.Architecture.Stairs:     [
                                (DB.BuiltInParameter.STAIRS_BASE_LEVEL_PARAM, DB.BuiltInParameter.STAIRS_BASE_OFFSET),
                                (DB.BuiltInParameter.STAIRS_TOP_LEVEL_PARAM, DB.BuiltInParameter.STAIRS_TOP_OFFSET)
                                ]
    }


# Select Elements
selection = uidoc.Selection.GetElementIds() or uidoc.Selection.PickObjects(UI.Selection.ObjectType.Element)
elements = [doc.GetElement(id) for id in selection]

# Select level
levels = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
# levels_dict = {"{} ({})".format(level.Name, level.Elevation): level for level in levels}
#
# levels_dict = OrderedDict(sorted(levels_dict.items(), key=lambda (key, value): value.Elevation, reverse=True))
# level_key = forms.SelectFromList.show(levels_dict.keys(), button_name='Select Level', multiple=False, message='Select level to change to.')
# level = levels_dict.get(level_key) # Using get() to avoid error message when cancelling dialog.


levels_dict = {"{}".format(level.Name): level for level in levels}

# TODO: Make interface for creating mapping dict.
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
    "Spor":   "U6",
    "U6":   "U6"
    }


if elements:
    with DB.Transaction(doc, __title__) as t:
        t.Start()

        for element in elements:
            # print(element)
            builtin_parameters = builtin_parameter_mapping.get(type(element))

            if not builtin_parameters:
                print("{} not yet supported".format(type(element)))

            elif isinstance(builtin_parameters, list):
                for level_builtin, offset_builtin in builtin_parameters:
                    # print(level_builtin, offset_builtin)
                    level_ex = doc.GetElement(element.get_Parameter(level_builtin).AsElementId())
                    if level_ex:
                        level = levels_dict[level_mapping_dict[level_ex.Name]]
                    else:
                        continue
                    element_change_level(element, level, level_builtin, offset_builtin)
            else:
                level_ex = doc.GetElement(element.get_Parameter(builtin_parameters[0]).AsElementId())
                level = levels_dict[level_mapping_dict[level_ex.Name]]
                element_change_level(element, level, builtin_parameters[0], builtin_parameters[1])

        t.Commit()


# Log write test
# import os
# log_path = os.path.join(__commandpath__, 'test.log')
# # print(log_path)
#
# with open(log_path, 'w') as f:
#     f.write('Hello World!')
