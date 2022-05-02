# -*- coding: utf-8 -*-

from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

import antler

import math


logger = script.get_logger()
output = script.get_output()


current_selection = revit.uidoc.Selection.GetElementIds() or script.exit()
elements = [revit.doc.GetElement(id) for id in current_selection]


common_definitions = antler.parameters.get_common_parameter_definitions(
    elements, filter_function=lambda x: x.StorageType in (DB.StorageType.Integer, DB.StorageType.Double))
logger.debug(common_definitions)


if not common_definitions:
    logger.warning("Elements does not have any common valid parameters.")
    script.exit()


# if EXEC_PARAMS.config_mode:
parameter_definition_dict = {
    definition.Name: definition for definition in common_definitions}
logger.debug(parameter_definition_dict)

selected_definition_key = forms.SelectFromList.show(
    sorted(parameter_definition_dict.keys()),
    title='Select Parameter to set',
    multiselect=False
) or script.exit()

definition = parameter_definition_dict[selected_definition_key]


existing_values_set = list(set([
    antler.parameters.get_parameter_value(element.get_Parameter(definition)) for element in elements
]))

if len(existing_values_set) == 1:
    existing_value = existing_values_set[0]
else:
    existing_value = ""

new_value = forms.ask_for_string(
    default=str(existing_value),
    prompt='Enter new parameter value',
    title='New Parameter Value'
)

with DB.Transaction(revit.doc, "Set Parameter Values") as t:
    t.Start()

    for element in elements:
        # with DB.Transaction(revit.doc, "Set Parameter Value") as t:
        #     t.Start()
        logger.debug("Element: {}".format(element))

        parameter = element.get_Parameter(definition)
        existing_value = antler.parameters.get_parameter_value(parameter)

        try:
            antler.parameters.set_parameter_value(parameter, new_value)
        except Exception as e:
            logger.warning(e)

            # t.Commit()
    t.Commit()
    # t.Assimilate()
