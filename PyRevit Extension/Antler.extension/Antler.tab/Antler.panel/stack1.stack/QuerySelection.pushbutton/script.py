# -*- coding: utf-8 -*-
import clr

from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

import antler

uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()
output = script.get_output()

def get_properties(obj):
    pass

elements = [doc.GetElement(id) for id in uidoc.Selection.GetElementIds()]

if not elements:
    category = antler.forms.select_category(multiselect=False)
    elements = antler.forms.select_types(categories=[category])

for element in elements:
    print("Element: {}".format(element))

    print("Element Type: {}".format(type(element)))

    # Tranformation
    output.print_md("### Transform")
    try:
        total_transform = element.GetTotalTransform()
        print(antler.util.query_transform(total_transform))
    except Exception as e:
        logger.warning(e)

    try:
        transform = element.GetTransform()
        print(antler.util.query_transform(transform))
    except Exception as e:
        logger.warning(e)


    # Location
    direction = antler.geometry.transform.element_direction(element)
    print("Direction: {direction}".format(direction=direction))


    output.print_md("### Location")
    location = element.Location

    try:
        print(clr.Convert(location, DB.LocationCurve))
    except Exception as e:
        logger.warning(e)

    try:
        print(clr.Convert(location, DB.LocationPoint).Point)
    except Exception as e:
        logger.warning(e)

    output.print_md("### Bounding Box")
    try:
        bbox = element.get_BoundingBox(revit.uidoc.ActiveView)
    except Exception as e:
        logger.warning(e)
    else:
        print([bbox.Min, bbox.Max])

    # print("\n\t Parameters")
    parameter_dict = {parameter.Definition.Name: parameter.AsString(
    ) or parameter.AsValueString() for parameter in element.Parameters}

    antler.util.print_dict_as_table(parameter_dict, title="Parameters", sort=True)


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
