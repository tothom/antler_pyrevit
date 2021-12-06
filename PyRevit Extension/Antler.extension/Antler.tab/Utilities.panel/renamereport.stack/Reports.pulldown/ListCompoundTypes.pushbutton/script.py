# -*- coding: utf-8 -*-

import antler
from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS
import re

uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()

# lib_path  = re.split('\w*\.extension', __commandpath__)[0] + 'lib'
# import sys
# if not lib_path in sys.path:
#     sys.path.append(lib_path)


# ELEMENT_TYPE_CONVERSION_DICT = {
#     DB.Wall: 'WallType',
#     DB.Floor: 'FloorType',
#     # DB.Roof: 'RoofType',
#     DB.FootPrintRoof: 'RoofType',
#     DB.Ceiling: 'Ceiling',
# }


def report_layer_structure(type_element):
    """
    """
    # logger.debug(type(element))
    #
    # type_element_id = element.GetTypeId()
    #
    # type_element = doc.GetElement(type_element_id)
    #
    # if not type_element:
    #     return None

    # type_element = eval(
    #     'element.' + ELEMENT_TYPE_CONVERSION_DICT[type(element)])
    # logger.debug(type_element)

    # Collect layer information
    compound_structure = type_element.GetCompoundStructure()

    layers_dict = antler.interop.compound_structure_to_dict(
        compound_structure)

    # Print layer information
    antler.util.print_dict_list([a.get('Material')
                              for a in layers_dict.values()])

    # Write layer string to parameter
    build_list = []

    for layer in layers_dict.values():
        layer_string = '-'

        material = layer['Material']

        if material:
            description = material['Description']

            if description:
                layer_string = description

        logger.debug(layer_string)
        build_list.append(layer_string)

    return build_list


# selection = uidoc.Selection.GetElementIds() or uidoc.Selection.PickObjects(
#     UI.Selection.ObjectType.Element, "Select objects to check.")

builtin_category = antler.forms.select_category()

category = antler.util.builtin_category_from_category(builtin_category)

elements = DB.FilteredElementCollector(revit.doc).OfCategory(category).WhereElementIsElementType().ToElements()

# elements = [doc.GetElement(id) for id in selection]

print_list = []

for element in elements:
    compound_structure = report_layer_structure(element)
    print_list.append(compound_structure)

print(print_list)
#
# with DB.Transaction(revit.doc, __commandname__) as t:
#     t.Start()
#

#
#         if EXEC_PARAMS.config_mode:
#             build_string = '\r\n'.join(build_list)
#
#             parameter = element_type.LookupParameter('Oppbygning')
#             parameter.Set(build_string)
#
#     t.Commit()
