# -*- coding: utf-8 -*-

from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

import antler

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

parameter_definition_dict = {
    definition.Name: definition for definition in common_definitions}
logger.debug(parameter_definition_dict)

selected_definition_key = forms.SelectFromList.show(
    sorted(parameter_definition_dict.keys()),
    title='Select Parameter to sum',
    multiselect=False
) or script.exit()

selected_definition = parameter_definition_dict[selected_definition_key]

internal_values = []

for element in elements:
    logger.debug("Element: {}".format(element))

    parameter = element.get_Parameter(selected_definition)
    internal_value = antler.parameters.get_parameter_internal_value(parameter, convert=False)
    internal_values.append(internal_value)

# internal_value_sum = sum(internal_values)

output.print_md(
    "Sum of parameter {definition} for {count} elements is **{formatted_value}**".format(
        definition=selected_definition_key,
        count=len(elements),
        value=sum(values),
        formatted_value=DB.UnitFormatUtils.Format(
            revit.doc.GetUnits(),
            selected_definition.UnitType,
            sum(internal_values),
            True,
            False)
    )
)
