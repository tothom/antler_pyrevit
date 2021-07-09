import decimal
import difflib
from rpw import revit, DB
import System.Enum


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
