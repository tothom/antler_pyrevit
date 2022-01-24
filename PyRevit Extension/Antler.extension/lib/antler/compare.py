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


class ElementMatcher():
    """
    Class to attempt find matching elements in other docs. It will find
    elements of matching class and category.
    """

    def __init__(self, element, other_doc):
        self.element = element
        self.other_doc = other_doc

        logger.info(self.element.Name)
        logger.info(self.element.Category.Name)

        self.match = self.match_by_name()

    def match_by_parameter(self):
        pass

    def match_by_name(self):
        logger.debug(self.element)
        name = self.element.Name

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

            other_name = iterator.Current.get_Parameter(
                DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()

            logger.info(other_name)

            if name == other_name:
                return iterator.Current
