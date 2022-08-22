# -*- coding: utf-8 -*-

from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

import antler

import math


logger = script.get_logger()
output = script.get_output()


current_selection = revit.uidoc.Selection.GetElementIds() or script.exit()
elements = [revit.doc.GetElement(id) for id in current_selection]


common_definitions = antler.parameters.get_definitions_from_elements(
    elements, filter_function=lambda x: x.StorageType in (DB.StorageType.Integer, DB.StorageType.Double))
logger.debug(common_definitions)


if not common_definitions:
    logger.warning("Elements does not have any common valid parameters.")
    script.exit()


if EXEC_PARAMS.config_mode:
    parameter_definition_dict = {
        definition.Name: definition for definition in common_definitions}
    logger.debug(common_definitions)

    selected_definition_keys = forms.SelectFromList.show(
        sorted(common_definitions_dict.keys()),
        title='Select Parameter to sum',
        multiselect=True
    ) or script.exit()

    definitions = [parameter_definition_dict[a] for a in selected_definition_keys]
else:
    definitions = common_definitions


report = []


for definition in definitions:
    internal_values = []

    logger.debug(definition.Name)
    logger.debug(definition.GetSpecTypeId())

    has_values = []

    for element in elements:
        logger.debug("Element: {}".format(element))

        parameter = element.get_Parameter(definition)
        internal_value = antler.parameters.get_parameter_value(parameter, convert=False)
        internal_values.append(internal_value)

        logger.debug(parameter.HasValue)

        has_values.append(parameter.HasValue)

    # internal_value_sum = sum(internal_values)

    if all(has_values):
        format_value = lambda x: DB.UnitFormatUtils.Format(
            revit.doc.GetUnits(),
            definition.GetSpecTypeId(),
            x,
            False)

        logger.debug(format_value(sum(internal_values)))

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
