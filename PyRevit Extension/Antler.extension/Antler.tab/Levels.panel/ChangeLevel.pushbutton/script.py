from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script
from collections import OrderedDict

import antler

__doc__ = "Changes Level of selected Elements without moving them."
__title__ = "Change Level"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()

def element_change_level(element, level_new, level_builtin, offset_builtin):
    """
    Changes Level of Roof to new Level without moving the Roof.
    """
    level_param = element.get_Parameter(
        level_builtin)  # DB.BuiltInParameter.ROOF_CONSTRAINT_LEVEL_PARAM
    # DB.BuiltInParameter.ROOF_CONSTRAINT_OFFSET_PARAM
    offset_param = element.get_Parameter(offset_builtin)

    level_ex = doc.GetElement(level_param.AsElementId())

    if level_ex:
        elevation_diff = level_ex.Elevation - level_new.Elevation
        offset_new = elevation_diff + offset_param.AsDouble()

        level_param.Set(level_new.Id)
        offset_param.Set(offset_new)

    return element


BUILTIN_PARAMETER_MAPPING = {
    DB.Floor:                   (DB.BuiltInParameter.LEVEL_PARAM, DB.BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM),
    DB.ExtrusionRoof:           (DB.BuiltInParameter.ROOF_CONSTRAINT_LEVEL_PARAM, DB.BuiltInParameter.ROOF_CONSTRAINT_OFFSET_PARAM),
    DB.FootPrintRoof:           (DB.BuiltInParameter.ROOF_BASE_LEVEL_PARAM, DB.BuiltInParameter.ROOF_LEVEL_OFFSET_PARAM),
    DB.FamilyInstance:          (DB.BuiltInParameter.FAMILY_LEVEL_PARAM, DB.BuiltInParameter.INSTANCE_SILL_HEIGHT_PARAM),
    DB.Ceiling:                 (DB.BuiltInParameter.LEVEL_PARAM, DB.BuiltInParameter.CEILING_HEIGHTABOVELEVEL_PARAM),
    DB.Group:                   (DB.BuiltInParameter.GROUP_LEVEL, DB.BuiltInParameter.GROUP_OFFSET_FROM_LEVEL),
    DB.Wall:                    [
        (DB.BuiltInParameter.WALL_BASE_CONSTRAINT,
         DB.BuiltInParameter.WALL_BASE_OFFSET),
        (DB.BuiltInParameter.WALL_HEIGHT_TYPE, DB.BuiltInParameter.WALL_TOP_OFFSET)
    ],
    DB.Opening:                 [
        (DB.BuiltInParameter.WALL_BASE_CONSTRAINT,
         DB.BuiltInParameter.WALL_BASE_OFFSET),
        (DB.BuiltInParameter.WALL_HEIGHT_TYPE, DB.BuiltInParameter.WALL_TOP_OFFSET)
    ],
    DB.Architecture.Stairs:     [
        (DB.BuiltInParameter.STAIRS_BASE_LEVEL_PARAM,
         DB.BuiltInParameter.STAIRS_BASE_OFFSET),
        (DB.BuiltInParameter.STAIRS_TOP_LEVEL_PARAM,
         DB.BuiltInParameter.STAIRS_TOP_OFFSET)
    ]
}


# Select Elements
selection = uidoc.Selection.GetElementIds() or uidoc.Selection.PickObjects(
    UI.Selection.ObjectType.Element)
elements = [doc.GetElement(id) for id in selection]

level = antler.forms.select_levels(multiselect=False)



if elements:
    with DB.Transaction(doc, __title__) as t:
        t.Start()

        for element in elements:
            # print(element)
            builtin_parameters = BUILTIN_PARAMETER_MAPPING.get(type(element))

            if not builtin_parameters:
                logger.warning("{} not yet supported".format(type(element)))

            elif isinstance(builtin_parameters, list):
                for level_builtin, offset_builtin in builtin_parameters:
                    element_change_level(
                        element, level, level_builtin, offset_builtin)
            else:
                element_change_level(
                    element, level, builtin_parameters[0], builtin_parameters[1])

        t.Commit()
