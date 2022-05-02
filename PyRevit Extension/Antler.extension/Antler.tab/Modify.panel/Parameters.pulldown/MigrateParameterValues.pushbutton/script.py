# -*- coding: utf-8 -*-

from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS


from System.Collections.Generic import List

import antler

import math


logger = script.get_logger()
output = script.get_output()


# current_selection = revit.uidoc.Selection.GetElementIds() or script.exit()
# elements = [revit.doc.GetElement(id) for id in current_selection]

# Select categories and collect elements
categories = antler.forms.select_category(multiselect=True)

category_list = List[DB.ElementId]([category.Id for category in categories])

collector = DB.FilteredElementCollector(
    revit.doc).WhereElementIsNotElementType()
multi_category_filter = DB.ElementMulticategoryFilter(category_list)
collector.WherePasses(multi_category_filter)

elements = collector.ToElements()

logger.debug(len(elements))

# Check for common parameters and select parameter to migrate.
common_definitions = antler.parameters.get_common_parameter_definitions(
    elements,
    filter_function=lambda x: x.StorageType in (
        DB.StorageType.Integer, DB.StorageType.Double, DB.StorageType.String)
)

# if EXEC_PARAMS.config_mode:
parameter_definition_dict = {
    definition.Name: definition for definition in common_definitions}

if len(common_definitions) != parameter_definition_dict:
    logger.warning("Parameters with duplicate names detected!")

logger.debug(parameter_definition_dict)

selected_source_definition_key = forms.SelectFromList.show(
    sorted(parameter_definition_dict.keys()),
    title='Select Parameter as source',
    multiselect=False
) or script.exit()

source_definition = parameter_definition_dict[selected_source_definition_key]


possible_destination_definitions = {k: v for k, v in parameter_definition_dict.items(
    ) if v.ParameterType == source_definition.ParameterType and v != source_definition}

if not possible_destination_definitions:
    logger.warning(
        "There are no possible destination parameters. Consider making a new parameter.")
    script.exit()
else:
    selected_destination_definition_key = forms.SelectFromList.show(
        sorted(possible_destination_definitions.keys()),
        title='Select Parameter as destination',
        multiselect=False
    ) or script.exit()

    destination_definition = possible_destination_definitions[
        selected_destination_definition_key]


# Check diff
def compare_parameter_values(element, source, destination, overwrite=False):
    source_parameter = element.get_Parameter(source)

    destination_parameter = element.get_Parameter(destination)

    source_value = antler.parameters.get_parameter_value(
        source_parameter, convert=False)

    destination_value = antler.parameters.get_parameter_value(
        destination_parameter, convert=False)

    if source_value is None:# or source_value in ("",):
        pass
    elif destination_value is None:
        pass
    elif overwrite and source_value != destination_value:


    return source_value, destination_value


    # if source_parameter.HasValue:
    #     source_value = antler.parameters.get_parameter_value(
    #         source_parameter, convert=False)
    #
    #     if destination_parameter.HasValue:
    #         destination_value = antler.parameters.get_parameter_value(
    #             destination_parameter, convert=False)
    #
    #         if source_value != destination_value:
    #             conflicts.append(
    #                 {
    #                     'Element': output.linkify(element.Id),
    #                     source_definition.Name: source_value,
    #                     destination_definition.Name: destination_value,
    #                 }
    #             )
    #
    #     if element.Document.IsModifable:
    #         antler.parameters.set_parameter_value(
    #             destination_parameter, source_value, convert=False)
for element in elements:
    print(compare_parameter_values(element, source_definition, destination_definition))

script.exit()

with DB.TransactionGroup(revit.doc, __commandname__) as tg:
    conflicts = []
    tg.Start()

    for element in elements:

        with DB.Transaction(revit.doc, "Copy parameter value") as t:
            t.Start()

            t.Commit()

    if conflicts:
        antler.util.print_dict_list(
            conflicts,
            title="Migration conflicts",
            columns=['Element', source_definition.Name,
                     destination_definition.Name]
        )
        tg.RollBack()
    else:
        print("No migration conflicts found.")
        tg.Commit()

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
