# -*- coding: utf-8 -*-
# from rpw import DB, revit
from pyrevit import forms, script

# import antler

import hashlib
import uuid

import re

from System.Windows.Forms import Clipboard

logger = script.get_logger()

seeds = ""

if Clipboard.ContainsText():
    seeds = re.split('\r\n', Clipboard.GetText())

if not seeds:
    seed_input = forms.ask_for_string(
        prompt="Enter seed values",
        title="GUID Seed"
    ) or script.exit()

    seeds = re.split('[;]', seed_input) or script.exit()



# logger.info(seeds)
c = 1

for seed in seeds:
    seed = seed.strip()

    logger.debug("'{seed}'".format(seed=seed))

    if seed:
        m = hashlib.md5()
        m.update(seed.encode('utf-8'))
        new_uuid = uuid.UUID(m.hexdigest())

        print(new_uuid)

        c += 1

logger.info(c)
#
# # select_compound_classes
# compound_classes = [
#     DB.Floor,
#     DB.RoofBase,
#     DB.Wall,
#     DB.Ceiling
# ]
#
# # select_compound_classes
# compound_categories_dict = {
#     'Floors': DB.BuiltInCategory.OST_Floors,
#     'Walls': DB.BuiltInCategory.OST_Walls,
#     # 'RoofBase',
#     # 'Wall',
#     # 'Ceiling'
# }
#
# selected = forms.SelectFromList.show(
#     sorted(compound_categories_dict.keys()),
#     button_name='Select Categories',
#     multiselect=False
# )
#
#
# builtin_category = compound_categories_dict[selected]
#
# logger.debug(builtin_category)

#
# # for doc in docs:
# type_elements = DB.FilteredElementCollector(revit.doc).WhereElementIsElementType().ToElements()
#
# logger.debug(type_elements)
#
# # report_dict = OrderedDict()
#
# report = []
#
# text_parameters = antler.parameters.get_all_parameters(
#     elements,
#     hashable_provider=antler.parameters.parameter_name_string_provider,
#     parameters_provider=lambda x:x.ParametersMap,
#     filter_function=lambda x:x.Definition.ParameterType == DB.ParameterType.Text
#     )
#
# hash_parameter = forms.SelectFromList.show(
#     sorted(text_parameters),
#     title="Select hashing parameter",
#     multiselect=False
# ) or script.exit()
#
# guid_parameter = forms.SelectFromList.show(
#     sorted(text_parameters),
#     title="Select GUID parameter",
#     multiselect=False
# ) or script.exit()
#
# with DB.Transaction(revit.doc, __commandname__) as t:
#     t.Start()
#
#     for type_element in type_elements:
#         compound_structure = type_element.GetCompoundStructure()
#
#         layer_string = antler.parameters.compound_structure_summary(
#             antler.parameters.minimal_layer_string, sep='-'),
#
#         parameter = element_type.LookupParameter(guid_parameter)
#
#         antler.parameters.set_parameter_value(parameter, layer_string)
#
#     t.Commit()
