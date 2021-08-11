from rpw import revit, DB
from pyrevit import forms, script

import clr

import util

import System.Drawing

logger = script.get_logger()


def select_element_parameters(element):
    definition_dict = {
        parameter.Definition.Name: parameter.Definition
        for parameter in element.Parameters}

    selected_definitions = forms.SelectFromList.show(
        sorted(definition_dict.keys()),
        title='Select Parameters',
        multiselect=True
    )

    return selected_definitions  # TODO: Return Parameter objects, not just strings


def select_instance_parameters_of_category(category, doc=revit.doc):
    """

    """
    # TODO: Does not work well on familyinstances such as doors. All instances must be processed to make this work.
    builtin_category = util.builtin_category_from_category(category)

    element = DB.FilteredElementCollector(doc).OfCategory(
        builtin_category).WhereElementIsNotElementType().FirstElement()

    parameters_dict = {e.Definition.Name: e for e in element.ParametersMap}

    parameters_selected = forms.SelectFromList.show(
        sorted(parameters_dict.keys()),
        title='Select Parameters',
        multiselect=True
    )

    return [parameters_dict[a] for a in parameters_selected]


def select_category(doc=revit.doc):
    """
    """
    categories_dict = {c.Name: c for c in doc.Settings.Categories}

    categories_selected = forms.SelectFromList.show(
        sorted(categories_dict.keys()),
        button_name='Select Categories',
        multiselect=True
    )

    logger.debug(categories_selected)

    return [categories_dict[a] for a in categories_selected]

    # category_found = Revit.Elements.Category.ByName(str(category))


def print_dict_list(dict_list, title=""):
    """Prints a list of dictionaries as a table with keys as column names.
    """
    columns = []

    for row in dict_list:
        columns.extend(row.keys())

    columns = sorted(list(set(columns)))

    data = []

    for item in dict_list:
        data_row = []

        for key in columns:
            data_row.append(item.get(key, '-'))

        data.append(data_row)

    output = script.get_output()

    output.print_table(
        table_data=data,
        title=title,
        columns=columns
    )

def quick_color_element(element, color):
    """"""
    line_color = color
    fill_color = lighten_color(color)



def lighten_color(color, factor=0.5):
    r, g, b = color.R, color.G, color.B
    # Do something
    return System.Drawing.Color.FromArgb(r, g, b)
