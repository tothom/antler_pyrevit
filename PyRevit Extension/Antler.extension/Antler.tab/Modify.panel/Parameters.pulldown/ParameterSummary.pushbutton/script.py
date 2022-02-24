# -*- coding: utf-8 -*-

from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

import antler

import math

uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()
output = script.get_output()


current_selection = uidoc.Selection.GetElementIds() or script.exit()
elements = [doc.GetElement(id) for id in current_selection]


common_definitions = antler.parameters.get_common_parameter_definitions(
    elements, filter_function=lambda x: x.StorageType in (DB.StorageType.Integer, DB.StorageType.Double))
logger.debug(common_definitions)


if not common_definitions:
    logger.warning("Elements does not have any common valid parameters.")
    script.exit()


if EXEC_PARAMS.config_mode:
    parameter_definition_dict = {
        definition.Name: definition for definition in common_definitions}
    logger.debug(parameter_definition_dict)

    selected_definition_keys = forms.SelectFromList.show(
        sorted(parameter_definition_dict.keys()),
        title='Select Parameter to sum',
        multiselect=True
    ) or script.exit()

    definitions = [parameter_definition_dict[a] for a in selected_definition_keys]
else:
    definitions = common_definitions


report = []

for definition in definitions:
    internal_values = []

    for element in elements:
        logger.debug("Element: {}".format(element))

        parameter = element.get_Parameter(definition)
        internal_value = antler.parameters.get_parameter_value(parameter, convert=False)
        internal_values.append(internal_value)

    # internal_value_sum = sum(internal_values)

    format_value = lambda x:DB.UnitFormatUtils.Format(
        revit.doc.GetUnits(),
        definition.UnitType,
        x,
        True,
        False)

    parameter_summary = {
        'Parameter': definition.Name,
        'Minimum': format_value(min(internal_values)),
        'Maximum': format_value(max(internal_values)),
        'Sum': format_value(sum(internal_values)),
        'Average': format_value(sum(internal_values)/len(internal_values)),
    }

    report.append(parameter_summary)

antler.util.print_dict_list(
    report,
    title="Parameter Summary",
    sort_key='Parameter',
    columns=['Parameter', 'Sum', 'Minimum', 'Maximum', 'Average']
    )

    # output.print_md(
    #     "Sum of parameter {definition} for {count} elements is **{formatted_value}**".format(
    #         definition=definition_key,
    #         count=len(elements),
    #         formatted_value=DB.UnitFormatUtils.Format(
    #             revit.doc.GetUnits(),
    #             definition.UnitType,
    #             sum(internal_values),
    #             True,
    #             False)
    #     )
    # )
