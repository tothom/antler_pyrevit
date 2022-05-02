"""
Contains helper functions for Antler. It could be converters, formatters,
simple general functions etc...
"""
from rpw import revit, DB
from pyrevit import forms, script

import decimal
import difflib
import System.Enum

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


def step_centered_range(min, max, step_min):
    max = float(max)
    min = float(min)
    step_min = float(step_min)

    assert step_min > 0
    assert max > min

    step = (max - min) / (math.floor((max - min) / step_min))

    n = min + (step / 2.0)

    while n < max:
        yield float(n)

        n += step

# values = [a for a in step_centered_range(120, 210, 7)]
#
# print(values)

def builtin_category_from_category(category):
    """
    Returns corresponding Builtin Category from Category.
    """
    logger.debug(type(category))

    if isinstance(category, DB.BuiltInCategory):
        return category

    for builtin_category in System.Enum.GetValues(DB.BuiltInCategory):
        if DB.ElementId(builtin_category).IntegerValue == category.Id.IntegerValue:
            return builtin_category

    return None

# def assure_builtin_category(category):
#     if isinstance(category, DB.)


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
    logger.debug(matches)

    new_string = template_string

    for match in matches:
        logger.debug(match)
        # parameter_name = match.string[1:-1] # Python 3

        match_substring = match.string[match.start():match.end()]
        parameter_name = match_substring[1:-1]

        logger.debug(parameter_name)

        parameter = element.LookupParameter(parameter_name)

        if not parameter:
            raise ValueError("Parameter '{}' not found".format(parameter_name))

        value = parameter.AsString() or parameter.AsValueString() or ""

        if not value:
            logger.warning(
                "Parameter '{}' has empty value".format(parameter_name))

        logger.debug("{parameter}: {value}".format(
            parameter=parameter_name, value=value))

        new_string = new_string.replace(match_substring, value)

    return new_string


def random_numbers(seed, count=1):
	"""
	Returns a list of random numbers from given seed. The seed can be anything: numbers, strings, class instances and so on.
	"""
	from System import Random

	rand = Random(int(hash(seed)))
	numbers = [rand.NextDouble() for _ in range(count)]

	return numbers


# def print_dict_list_as_table(dict_list, title="", formats=[], sort_key=None):
#     output = script.get_output()
#
#     keys = set().union(*(d.keys() for d in dict_list))
#
#     if not formats:
#         formats = ['' for _ in keys]
#
#     output.print_table(
#         table_data=[[a.get(k) for k in keys] for a in dict_list],
#         title=title,
#         columns=keys,
#         formats=formats
#     )


def print_dict_as_table(dictionary, title="", columns=(), formats=[], sort=False):
    output = script.get_output()

    data = []

    for k, v in dictionary.items():
        # Workaround because markdown interpreter does not allow line breaks in tables.
        # print("{}: {}".format(k, v))

        k = k.replace('\r\n', '')
        v = str(v).replace('\r\n', '')

        data.append((k, v))

    if sort:
        data = sorted(data, key=lambda x:x[0].lower())

    output.print_table(
        table_data=data,
        title=title,
        columns=columns or ('Key', 'Value'),
        formats=formats or ('', '')
    )


def dict_list_to_array(
        dict_list,
        columns=[],
        sort_key=None,
        not_found_str='',
        none_str='',
        replacements={}
        #{None: lambda x:''} # type: replacement_func
        # replace_line_breaks=False
        ):
    """
    Returns column headers and a organised list of data in a list of rows, where
    each row cell corresponds to the headers. Input must be a list of
    dictionaries.
    """
    if not columns:
        for row in dict_list:
            for key in row.keys():
                if not key in columns:
                    columns.append(key)

    dict_list = sorted(dict_list, key=lambda x: x.get(sort_key))

    data = []

    for dict_item in dict_list:
        data_row = []

        for key in columns:
            value = dict_item.get(key, not_found_str)

            if value is None:
                value = none_str

            logger.debug(value)
            data_row.append(value)

        data.append(data_row)

    return columns, data

def print_dict_list(dict_list, title="", sort_key=None, columns=[]):
    """Prints a list of dictionaries as a table with keys as column names.
    """
    columns, data = dict_list_to_array(
        dict_list, sort_key=sort_key, columns=columns,
        not_found_str='*N/A*', none_str='*None*')

    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            cell = str(cell).replace('\r\n', '<br/>')
            data[i][j] = cell

    output = script.get_output()

    output.print_table(
        table_data=data,
        title=title,
        columns=columns
    )



def close_revit():
    """
    BTW: Doesn't work. :) WIP
    """
    import System.Diagnostics
    import ctypes

    processes = System.Diagnostics.Process.GetCurrentProcess()

    if processes.Length > 0:
        revit_handle = processes[0].MainWindowHandle

        logger.info(revit_handle)
    # else:
    #     return

    WM_CLOSE = 0x10
