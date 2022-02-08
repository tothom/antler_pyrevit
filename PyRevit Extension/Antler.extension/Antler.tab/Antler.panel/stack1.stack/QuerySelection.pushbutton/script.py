# -*- coding: utf-8 -*-

from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

import antler

uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()

def get_properties(obj):
    pass

current_selection = uidoc.Selection.GetElementIds()

# print(current_selection)

selection = current_selection# or uidoc.Selection.PickObjects(
    # UI.Selection.ObjectType.Element, "Select objects to expand.")

elements = [doc.GetElement(id) for id in selection]

if not elements:
    category = antler.forms.select_category(multiselect=False)

    elements = antler.forms.select_types(categories=[category])

for element in elements:
    print("Element: {}".format(element))

    # print("\n\t Parameters")
    parameter_dict = {parameter.Definition.Name: parameter.AsString(
    ) or parameter.AsValueString() for parameter in element.Parameters}

    antler.util.print_dict_as_table(parameter_dict, title="Parameters", sort=True)

    # for k, v in parameter_dict.items():
    #     print(k, v)

    # print("\n\t Parameters Map")
    # parameters_map = {parameter.Definition.Name: parameter.AsString(
    # ) or parameter.AsValueString() for parameter in element.ParametersMap}
    #
    # for k, v in parameters_map.items():
    #     print(k, v)

    # print("\n\t dir(element.Parameters)")
    # for attr in dir(element.Parameters):
    #     try:
    #         value = getattr(element.Parameters, attr)
    #         if not callable(value):
    #             print(attr, value, type(value))  # , callable(value))
    #     except Exception as e:
    #         print(e)

    # print("\n\t dir() -> Element Properties")

    element_property_dict = {}

    for attr in dir(element):
        try:
            value = getattr(element, attr)
            if not callable(value):
                # print(attr, value, type(value))  # , callable(value))
                element_property_dict[attr] = value
        except Exception as e:
            print(e)

    antler.util.print_dict_as_table(element_property_dict, title="dir() -> Element Properties", sort=True)

    try:
        element_type = doc.GetElement(element.GetTypeId())
        print("Element Type: {}".format(element_type))

        # print("\n\t Type Parameters")
        type_parameter_dict = {parameter.Definition.Name: parameter.AsString(
        ) or parameter.AsValueString() for parameter in element_type.Parameters}

        antler.util.print_dict_as_table(type_parameter_dict, title="Type Parameters", sort=True)

        # print("\n".join(["{}: {}".format(k, v)
        #       for k, v in type_parameter_dict.items()]))
        # for k, v in type_parameter_dict.items():
        #     print(k, v)

        type_property_dict = {}

        # print("\n\t dir() -> Type Properties")
        for attr in dir(element):
            try:
                value = getattr(element, attr)
                if not callable(value):
                    # print(attr, value, type(value))  # , callable(value))
                    type_property_dict[attr] = value

            except Exception as e:
                print(e)

        antler.util.print_dict_as_table(type_property_dict, title="dir() -> Type Properties", sort=True)


    except:
        print("Element does not have a Type...\n")
