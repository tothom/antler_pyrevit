import antler.parameters
from rpw import revit, DB
from rpw.exceptions import RevitExceptions
from pyrevit import forms, script

import parameters

import hashlib

import clr

from System.Collections.Generic import IEnumerable

clr.AddReference("System.Core")
import System
clr.ImportExtensions(System.Linq)




logger = script.get_logger()
output = script.get_output()

def compare_parameters(source_parameter, destination_parameter):
    pass


def diff_elements(source_element, destination_element, exceptions=[]):
    """
    Returns parameters in destination element which are different from source
    element.

    Parameters in source element which does not exist in destination element,
    are not compared.

    Function does not test the category, family or type differences between the
    elements.
    """
    # diff = []
    diff_dict_list = []

    for source_parameter in source_element.Parameters:
        definition = source_parameter.Definition

        source_value = antler.parameters.get_parameter_value(source_parameter)

        if source_value is None or definition.Name in exceptions:
            continue

        # destination_parameter = destination_element.get_Parameter(definition)
        destination_parameter = destination_element.LookupParameter(definition.Name)

        if destination_parameter:
            destination_value = antler.parameters.get_parameter_value(
                destination_parameter)

            equal = source_value == destination_value

            if not equal:
                # diff_parameters[destination_parameter] = source_value
                # diff.append(definition)

                diff_dict_list.append({
                    'Definition': definition,
                    'Source': source_element,
                    'Destination': destination_element,
                    'Value': source_value,
                    # 'Status': status
                })

                logger.info("{equal}: {source}: '{source_value}' - {dest}: '{dest_value}'".format(
                    source=source_parameter.Definition.Name,
                    source_value=source_value,
                    equal='EQUAL' if equal else 'DIFF',
                    dest=destination_parameter.Definition.Name if destination_parameter else 'N/A',
                    dest_value=destination_value
                ))
        else:
            logger.warning("Parameter with name {name} not found in destination.".format(
                name=definition.Name
            ))

    # return diff_parameters
    return diff_dict_list



def print_diff(diff_parameters):

    output.print_md("**{}**".format(definition.Name))

    output.print_md("{source}\t**{equal}**\t{dest}".format(
        source=source_value,
        equal='==' if equal else '!=',
        dest=destination_value)
    )


def find_by_category():
    pass



def find_similar_element(element, doc, parameter=DB.BuiltInParameter.ALL_MODEL_TYPE_NAME):
    # Assures that input element is of class ElementType
    # element = clr.Convert(element, DB.ElementType)

    # category_filter
    # builtin_category = antler.util.builtin_category_from_category(
    #     element.Category)
    category_filter = DB.ElementCategoryFilter(element.Category.Id)

    # parameter_filter
    if isinstance(parameter, basestring):
        element_parameter = element.LookupParameter(parameter)
    else:
        element_parameter = element.get_Parameter(parameter)

    if not element_parameter.HasValue:
        return

    parameter_value = element_parameter.AsString()

    if parameter_value == '':
        return

    logger.debug(parameter_value)

    provider = DB.ParameterValueProvider(DB.ElementId(parameter))
    rule = DB.FilterStringRule(
        provider, DB.FilterStringEquals(), parameter_value, False)
    name_parameter_filter = DB.ElementParameterFilter(rule)

    # combine_two_filters
    logical_and_filter = DB.LogicalAndFilter(
        category_filter, name_parameter_filter)

    # get_collector
    collector = DB.FilteredElementCollector(doc)

    if isinstance(element, DB.ElementType):
        collector.WhereElementIsElementType()
    else:
        collector.WhereElementIsNotElementType()
    collector.WherePasses(logical_and_filter)

    count = collector.GetElementCount()

    logger.debug("Collector element count: {}".format(count))

    if count == 0:
        return None
    elif count == 1:
        return collector.FirstElement()
    else:
        raise KeyError("More than one element found.")
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
        #builtin_category = antler.util.builtin_category_from_category(category)
        category_filter = DB.ElementCategoryFilter(category.Id)

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


def match_project_parameter(project_parameter_binding, doc):
    matches = []

    iterator = revit.doc.ParameterBindings.ForwardIterator()
    iterator.Reset()

    while iterator.MoveNext():
        pass
