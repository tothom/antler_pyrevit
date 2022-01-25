import antler.parameters
from rpw import revit, DB
from rpw.exceptions import RevitExceptions
from pyrevit import forms, script

import clr

logger = script.get_logger()
output = script.get_output()


def diff_elements(source_element, destination_element):
    """
    Returns parameters in destination element which are different from source
    element.

    Parameters in source element which does not exist in destination element,
    are not compared.

    Function does not test the category, family or type differences between the
    elements.
    """

    diff_parameters = {}

    for source_parameter in source_element.ParametersMap:
        definition = source_parameter.Definition
        output.print_md("**{}**".format(definition.Name))

        destination_parameter = destination_element.get_Parameter(definition)

        source_value = antler.parameters.get_parameter_value(source_parameter)
        destination_value = antler.parameters.get_parameter_value(
            destination_parameter)

        equal = source_value == destination_value

        output.print_md("{source}\t{equal}\t{dest}".format(
            source=source_value,
            equal='==' if equal else '!=',
            dest=destination_value)
        )

        if not equal:
            diff_parameters[destination_parameter] = source_value

    return diff_parameters


class Finder():
    """
    Usage:

    Provide a minimum set of hints. At least an element or a parameter value
    must be provided.

    parameter_value_hints is a dict with parameters as keys and parameter
    values as values:
        {
            DB.BuiltInParameter.ALL_MODEL_TYPE_NAME: "Element Name",
            DB.Parameter: 50.0,
            "Height": 2400.0
        }
    """
    def __init__(
        self,
        doc,
        value_hint=None,
        element_hint=None,
        category_hint=None,
        class_hint=None,
        parameter_value_hints={}
        ):


        pass



def find_by_category():
    pass


def find_similar_by_parameter(
        element, doc, parameter=DB.BuiltInParameter.ALL_MODEL_TYPE_NAME):
    """
    Searches for similar element in input doc. The doc should be other doc than
    the doc where the element resides. By default the functions uses Type Name
    parameter as comparison parameter, by this can be changed. Only string
    parameters are supported as of now.
    """
    search_value = element.get_Parameter(
        parameter).AsString()

    builtin_category = antler.util.builtin_category_from_category(
        self.element.Category)

    collector = DB.FilteredElementCollector(
        self.other_doc).OfCategory(builtin_category).WhereElementIsElementType()

    logger.debug("Collector element count: {}".format(
        collector.GetElementCount()))

    iterator = collector.GetElementIterator()
    iterator.Reset()

    while iterator.MoveNext():
        logger.debug(iterator.Current)

        other_value = iterator.Current.get_Parameter(
            parameter).AsString()

        logger.debug(search_value, other_value)

        if search_value == other_value:
            return iterator.Current
