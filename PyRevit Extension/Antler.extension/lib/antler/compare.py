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

    Necessary hints:
        A string or an element or an element and a parameter

    Other hints:
        Parameters as {paramater: value} dict.
        category
        class
    """
    def __init__(
            self,
            doc,
            hints=[],
            ):

        self.doc = doc
        self.filters = []

        for hint in hints:
            if isinstance(hint, str):
                # Assumes the user is asking for element name
                self.add_type_name_parameter_filter(hint)

            if isinstance(hint, DB.ElementType):

                pass

            if isinstance(hint, (DB.BuiltInCategory, DB.Category)):
                self.add_category_filter(hint)

            if isinstance(hint, (DB.Parameter, DB.Definition)):
                pass

    def add_category_filter(self, category):
        builtin_category = antler.util.builtin_category_from_category(category)
        category_filter = DB.ElementCategoryFilter(builtin_category)

        self.filters.append(category_filter)

    def add_type_name_parameter_filter(self, name):
        provider = DB.ParameterValueProvider(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME)
        rule = DB.FilterStringRule(provider , DB.FilterStringContains(), hint, False)
        name_parameter_filter = DB.ElementParameterFilter(rule)

        self.filters.append(name_parameter_filter)



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
