# -*- coding: utf-8 -*-

import antler
from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS
import re
from System.Collections.Generic import List

uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()

# select_compound_classes
compound_classes = [
    DB.Floor,
    DB.RoofBase,
    DB.Wall,
    DB.Ceiling
]

# compound_classes_list = List[object](compound_classes)
#
# element_multiclassfilter = DB.ElementMulticlassFilter(compound_classes_list)
#
# element_types = DB.FilteredElementCollector(revit.doc).WhereElementIs

element_types = DB.FilteredElementCollector(revit.doc).OfCategory(DB.BuiltInCategory.OST_Floors).WhereElementIsElementType().ToElements()

# logger.info(element_types)

# element_type = eval(
#     'element.' + ELEMENT_TYPE_CONVERSION_DICT[type(element)])
# logger.info(element_type)

# Collect layer information

for element_type in element_types:
    logger.info(element_type.Name)
    compound_structure = element_type.GetCompoundStructure()

    # def compound_structure_to_dict(compound_structure):
    layers_dict = {}

    layer_string_list = []

    for layer in compound_structure.GetLayers():
        material_id = layer.MaterialId
        material = revit.doc.GetElement(material_id)

        material_dict = {}

        if material:
            material_dict = antler.interop.element_to_dict(material)
        #
        # layers_dict[layer.LayerId] = {
        #     'Function': layer.Function,
        #     'Width': layer.Width,
        #     'Material Id': layer.MaterialId.IntegerValue,
        #     'Material': material_dict,
        #     }

        layer_string = "{width} mm {material_name}".format(
            width=layer.Width*304.8,
            material_name=material_dict['Name']
        )

        layer_string_list.append(layer_string)

    compound_string = "\n".join(layer_string_list)

    logger.info(compound_string)

# return layers_dict

# layers_dict = antler.interop.compound_structure_to_dict(
#     compound_structure)
#
# # Print layer information
# antler.ui.print_dict_list([a.get('Material')
#                           for a in layers_dict.values()])

# Write layer string to parameter
# build_list = []
#
# for layer in layers_dict.values():
#     layer_string = '-'
#
#     material = layer['Material']
#
#     if material:
#         description = material['Description']
#
#         if description:
#             layer_string = description
#
#     logger.info(layer_string)
#     build_list.append(layer_string)
#
# return build_list
#
#
# selection = uidoc.Selection.GetElementIds() or uidoc.Selection.PickObjects(
#     UI.Selection.ObjectType.Element, "Select objects to check.")
#
# elements = [doc.GetElement(id) for id in selection]
#
# with DB.Transaction(revit.doc, __commandname__) as t:
#     t.Start()
#
#     for element in elements:
#         build_list = report_layer_structure(element)
#
#         if EXEC_PARAMS.config_mode:
#             build_string = '\r\n'.join(build_list)
#
#             parameter = element_type.LookupParameter('Oppbygning')
#             parameter.Set(build_string)
#
#     t.Commit()
