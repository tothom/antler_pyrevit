# from rpw import revit, DB
from pyrevit import forms, script

def select_element_parameters(element):
    definition_dict = {
        parameter.Definition.Name: parameter.Definition
        for parameter in element.Parameters}

    selected_definitions = forms.SelectFromList.show(
        sorted(definition_dict.keys()),
        title='Select Parameters',
        multiselect=True
    )

    return selected_definitions

def print_dict_list(dict_list, title=""):
    # Collect all keys and set as table columns
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
