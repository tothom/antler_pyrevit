# -*- coding: utf-8 -*-
from rpw import DB, revit
from pyrevit import forms, script

from collections import OrderedDict

import antler

logger = script.get_logger()



# select_compound_classes
compound_classes = [
    DB.Floor,
    DB.RoofBase,
    DB.Wall,
    DB.Ceiling
]

# select_compound_classes
compound_categories_dict = {
    'Floors': DB.BuiltInCategory.OST_Floors,
    'Walls': DB.BuiltInCategory.OST_Walls,
    # 'RoofBase',
    # 'Wall',
    # 'Ceiling'
}

selected = forms.SelectFromList.show(
    sorted(compound_categories_dict.keys()),
    button_name='Select Categories',
    multiselect=False
)


builtin_category = compound_categories_dict[selected]

logger.debug(builtin_category)


# for doc in docs:
type_elements = DB.FilteredElementCollector(revit.doc).OfCategory(
    builtin_category).WhereElementIsElementType().ToElements()

logger.debug(type_elements)

# report_dict = OrderedDict()

report = []

text_parameters = antler.parameters.get_all_parameters(
    elements,
    hashable_provider=antler.parameters.parameter_name_string_provider,
    parameters_provider=lambda x:x.ParametersMap,
    filter_function=lambda x:x.Definition.ParameterType == DB.ParameterType.Text
    )

parameter_to_write_to = forms.SelectFromList.show(
    sorted(text_parameters),
    title="Select parameter to write text string to.",
    multiselect=False
)

with DB.Transaction(revit.doc, __commandname__) as t:
    t.Start()

    for type_element in type_elements:
        compound_structure = type_element.GetCompoundStructure()

        layer_string = antler.parameters.compound_structure_summary(
            antler.parameters.minimal_layer_string, sep='-'),

        parameter = element_type.LookupParameter(parameter_to_write_to)

        antler.parameters.set_parameter_value(parameter, layer_string)

    t.Commit()
