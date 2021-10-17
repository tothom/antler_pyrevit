import decimal
import difflib
from rpw import revit, DB
import System.Enum

from pyrevit import script

logger = script.get_logger()


def best_fuzzy_match(str_list, search_str, min=0.33):
    ratios = [(c, difflib.SequenceMatcher(None, search_str, c).ratio())
              for c in str_list]

    ratios_sorted = sorted(ratios, key=lambda x: x[1])

    best_match = ratios_sorted[-1]

    if best_match[1] > min:
        return best_match[0]
    else:
        return None


def drange(x, y, jump):
    """source: https://stackoverflow.com/questions/7267226/range-for-floats
    """
    assert jump > 0, "Jump variable must be > 0."
    while x < y:
        yield float(x)
        x += decimal.Decimal(jump)


def builtin_category_from_category(category):
    """
    Returns corresponding Builtin Category from Category.
    """
    for builtin_category in System.Enum.GetValues(DB.BuiltInCategory):
        if DB.ElementId(builtin_category).IntegerValue == category.Id.IntegerValue:
            return builtin_category
    return None


def string_from_template(element, template_string):
    import re
    """
    Use "... {Parameter Name} ... {Other Parameter Name} ..." to create strings from Elements.

    Usage:
    string_from_template(element, "{Comments} - {Mark}")

    Returns "Some comment - 123"
    """
    pattern = '\{.*?\}'
    pattern_compiled = re.compile(pattern)

    matches = re.finditer(pattern_compiled, template_string)
    logger.info(matches)

    new_string = template_string

    for match in matches:
        logger.info(match)
        # parameter_name = match.string[1:-1] # Python 3

        match_substring = match.string[match.start():match.end()]
        parameter_name = match_substring[1:-1]

        logger.info(parameter_name)

        parameter = element.LookupParameter(parameter_name)

        if not parameter:
            raise ValueError, "Parameter '{}' not found".format(parameter_name)

        value = parameter.AsString() or parameter.AsValueString() or ""

        if not value:
            logger.warning(
                "Parameter '{}' has empty value".format(parameter_name))

        logger.info("{parameter}: {value}".format(
            parameter=parameter_name, value=value))

        new_string = new_string.replace(match_substring, value)

    return new_string


def preselect(revit_class=()):
    selected_element_ids = revit.uidoc.Selection.GetElementIds()

    filtered_elements = []

    for element_id in selected_element_ids:
        element = revit.doc.GetElement(element_id)

        if isinstance(element, revit_class) or not revit_class:
            filtered_elements.append(element)

    return filtered_elements


def random_numbers(seed, count=1):
	"""
	Returns a list of random numbers from given seed. The seed can be anything: numbers, strings, class instances and so on.
	"""
	from System import Random

	rand = Random(int(hash(seed)))
	numbers = [rand.NextDouble() for _ in range(count)]

	return numbers
