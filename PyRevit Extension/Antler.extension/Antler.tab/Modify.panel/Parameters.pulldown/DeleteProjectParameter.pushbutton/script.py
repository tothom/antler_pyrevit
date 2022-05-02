# -*- coding: utf-8 -*-

from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

from System.Collections.Generic import List

import antler

logger = script.get_logger()
output = script.get_output()

def delete_project_parameter(definition, doc=revit.doc, check_for_values=True):
    output = script.get_output()
    output.print_md("# {name}".format(name=definition.Name))
    output.set_width(300)

    try:
        binding = doc.ParameterBindings.get_Item(definition)
    except Exception as e:
        logger.warning(e)
        return

    logger.debug(binding)

    categories = List[DB.ElementId]([a.Id for a in binding.Categories])

    collector = DB.FilteredElementCollector(revit.doc)

    if isinstance(binding, DB.InstanceBinding):
        collector.WhereElementIsNotElementType()
    elif isinstance(binding, DB.TypeBinding):
        collector.WhereElementIsElementType()
    else:
        raise ValueError

    multi_category_filter = DB.ElementMulticategoryFilter(categories)
    collector.WherePasses(multi_category_filter)

    elements = collector.ToElements()

    logger.debug(len(elements))

    values = []

    delete = False

    if check_for_values:
        print("Checking for values...")

        for element in elements:
            parameter = element.get_Parameter(definition)

            if parameter and parameter.HasValue:
                value = antler.parameters.get_parameter_value(parameter)

                values.append({
                    'Element': output.linkify(element.Id),
                    'Value': value
                })

        if values:
            antler.util.print_dict_list(
                values,
                title="Elements with values",
                columns=['Element', 'Value']
                )
            # selected_option = forms.CommandSwitchWindow.show(
            #     ["Delete!", "Cancel"],
            #     message='Parameter {name} has elements with values. Delete?'.format(name=definition.Name)
            selected_option = forms.alert(
                'Parameter {name} has elements with values. Delete?'.format(name=definition.Name),
                options=["Delete!", "Cancel"],
            ) or script.exit()

            if selected_option == "Delete!":
                delete = True
        else:
            print("No elements with values detected.")
            delete = True
    else:
        delete = True

    if delete:
            binding_map = revit.doc.ParameterBindings
            logger.debug(binding_map.Contains(definition))

            try:
                binding_map.Remove(definition)
            except Exception as e:
                logger.warning(e)
            else:
                print("Project Parameter {definition} deleted!".format(definition=definition.Name))
                logger.debug(binding_map.Contains(definition))

    else:
        print("Project parameter not deleted.")


project_parameter_bindings = antler.forms.select_project_parameters(multiselect=True) or script.exit()

choice = forms.CommandSwitchWindow.show(
    ["Check for values", "Do not check for values"]
    message="Check if parameter has elements with values?"
) or script.exit()

check_for_values = choice == "Check for values"

# logger.debug(project_parameter_bindings)

# with DB.TransactionGroup(revit.doc, __commandname__) as tg:
#     tg.Start()

with DB.Transaction(revit.doc, "Delete Project Parameters") as t:
    t.Start()

    for definition, binding in project_parameter_bindings:
        delete_project_parameter(definition, check_for_values=check_for_values)

    t.Commit()

    # tg.Assimilate()
