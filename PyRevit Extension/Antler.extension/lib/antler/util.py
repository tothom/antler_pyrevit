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


# source: https://stackoverflow.com/questions/7267226/range-for-floats


def drange(x, y, jump):
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
    pattern = '\{\w*\}'
    pattern_compiled = re.compile(pattern)

    matches = re.finditer(pattern_compiled, template_string)

    new_string = template_string

    for match in matches:
        match_substring = match.string[match.start():match.end()]

        # parameter_name = match.string[1:-1] # Python 3
        parameter_name = match_substring[1:-1]

        parameter = element.LookupParameter(parameter_name)

        if not parameter:
            raise ValueError, "Parameter '{}' not found".format(parameter_name)

        value = parameter.AsString() or ""

        if not value:
            logger.warning("Parameter '{}' has empty value".format(parameter_name))

        logger.info("{parameter}: {value}".format(parameter=parameter_name, value=value))

        new_string = new_string.replace(match_substring, value)

    return new_string
