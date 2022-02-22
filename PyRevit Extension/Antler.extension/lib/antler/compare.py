import antler.parameters
from rpw import revit, DB
from rpw.exceptions import RevitExceptions
from pyrevit import forms, script

import parameters

import hashlib

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
        logger.debug(source_parameter)

        definition = source_parameter.Definition

        source_value = antler.parameters.get_parameter_value(source_parameter)
        logger.debug(source_value)

        destination_parameter = destination_element.get_Parameter(definition)

        if not destination_parameter:
            destination_value = None
        else:
            destination_value = antler.parameters.get_parameter_value(
                destination_parameter)

        equal = source_value == destination_value

        if not equal:
            diff_parameters[destination_parameter] = source_value

    return diff_parameters

def print_diff(diff_parameters):

    output.print_md("**{}**".format(definition.Name))


    output.print_md("{source}\t**{equal}**\t{dest}".format(
        source=source_value,
        equal='==' if equal else '!=',
        dest=destination_value)
    )


def find_by_category():
    pass


def find_similar_element(element_type, doc, parameter=DB.BuiltInParameter.ALL_MODEL_TYPE_NAME):
    # Assures that input element is of class ElementType
    element_type = clr.Convert(element_type, DB.ElementType)

    # category_filter
    builtin_category = antler.util.builtin_category_from_category(
        element_type.Category)
    category_filter = DB.ElementCategoryFilter(builtin_category)

    # parameter_filter
    parameter_value = element_type.get_Parameter(parameter).AsString()

    logger.info(parameter_value)

    provider = DB.ParameterValueProvider(DB.ElementId(parameter))
    rule = DB.FilterStringRule(
        provider, DB.FilterStringEquals(), parameter_value, False)
    name_parameter_filter = DB.ElementParameterFilter(rule)

    # combine_two_filters
    logical_and_filter = DB.LogicalAndFilter(
        category_filter, name_parameter_filter)

    # get_collector
    collector = DB.FilteredElementCollector(doc).WhereElementIsElementType()
    collector.WherePasses(logical_and_filter)

    count = collector.GetElementCount()

    logger.debug("Collector element count: {}".format(count))

    if count == 0:
        return None
    elif count == 1:
        return collector.FirstElement()
    else:
        # raise KeyError
        return None

    # iterator = collector.GetElementIterator()
    # iterator.Reset()
    #
    # while iterator.MoveNext():
    #     logger.debug(iterator.Current)
    #
    #     other_value = iterator.Current.get_Parameter(
    #         parameter).AsString()
    #
    #     logger.debug(search_value, other_value)
    #
    #     if search_value == other_value:
    #         return iterator.Current


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
        provider = DB.ParameterValueProvider(
            DB.ElementId(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME))
        rule = DB.FilterStringRule(
            provider, DB.FilterStringContains(), hint, False)
        name_parameter_filter = DB.ElementParameterFilter(rule)

        self.filters.append(name_parameter_filter)


def hash_element_by_parameters(element, exceptions=[]):
    """
    Useful for tracing changes in element parameters. For example to see if a
    Element Type has changes since last time, you can compare hashes.
    """
    # logger.info(exceptions)

    parameter_dictionary = {}

    for parameter in element.ParametersMap:
        logger.debug(parameter.Definition.Name)
        in_exceptions = any([parameter.Id == a.Id for a in exceptions])

        if not in_exceptions:
            value = parameters.get_parameter_value(parameter, convert=False)
            key = parameter.Definition.Name

            parameter_dictionary[key] = value
        else:
            logger.debug("{} not included in hash".format(parameter.Definition.Name))

    fset = frozenset(parameter_dictionary.items())

    return hash(fset)

    # h = hashlib.sha1()
    # h.update(fset)
    # h.digest()
