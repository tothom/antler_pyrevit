# -*- coding: utf-8 -*-

from rpw import revit, DB, UI
from pyrevit import forms, script
import re

logger = script.get_logger()

# lib_path  = re.split('\w*\.extension', __commandpath__)[0] + 'lib'
# import sys
# if not lib_path in sys.path:
#     sys.path.append(lib_path)

import antler

__doc__ = "Get Element Material Layers"
__title__ = "Element Layers"
__author__ = "Thomas Holth"

ELEMENT_TYPE_CONVERSION_DICT = {
    DB.Wall: 'WallType',
    DB.Floor: 'FloorType',
    # DB.Roof: 'RoofType',
    DB.FootPrintRoof: 'RoofType',
    DB.Ceiling: 'Ceiling',
}

elements = [revit.doc.GetElement(id) for id in revit.uidoc.Selection.GetElementIds()]

# element = elements[0]  # TODO: Modify script for multiple elements.

with DB.Transaction(revit.doc, __title__) as t:
    t.Start()

    for element in elements:

        logger.info(type(element))

        element_type = eval('element.' + ELEMENT_TYPE_CONVERSION_DICT[type(element)])
        logger.info(element_type)

        # Collect layer information
        compound_structure = element_type.GetCompoundStructure()

        layers_dict = antler.interop.compound_structure_to_dict(compound_structure)

        # Print layer information
        antler.ui.print_dict_list([a.get('M,aterial') for a in layers_dict.values()])

        # Write layer string to parameter
        build_list = []

        for layer in layers_dict.values():
            layer_string = '-'

            material = layer['Material']

            if material:
                description = material['Description']

                if description:
                    layer_string = description

            logger.info(layer_string)
            build_list.append(layer_string)

        build_string = '\r\n'.join(build_list)

        parameter = element_type.LookupParameter('Oppbygning')
        parameter.Set(build_string)

    t.Commit()
