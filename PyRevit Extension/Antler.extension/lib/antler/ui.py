from rpw import revit, DB
from pyrevit import forms, script

import clr
from collections import OrderedDict


import util


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


def select_category(doc=revit.doc, multiselect=False):
    """
    """
    categories_dict = {c.Name: c for c in doc.Settings.Categories}

    selected = forms.SelectFromList.show(
        sorted(categories_dict.keys()),
        button_name='Select Categories',
        multiselect=multiselect
    )

    logger.debug(selected)

    if multiselect:
        return [categories_dict[a] for a in selected]
    else:
        return categories_dict[selected]

    # category_found = Revit.Elements.Category.ByName(str(category))


def select_of_class(revit_class, key_function, select_types=True, doc=revit.doc, **kwargs):
    collector = DB.FilteredElementCollector(doc)

    if select_types:
        collector.WhereElementIsElementType()
    else:
        collector.WhereElementIsNotElementType()

    collector.OfClass(revit_class)

    # for a in collector:
    #     print(a)
    elements = collector.ToElements()
    selection_dict = OrderedDict()

    for element in elements:
        key = key_function(element)
        selection_dict[key] = element

    selected = forms.SelectFromList.show(
        sorted(selection_dict.keys()),
        **kwargs
    )

    if selected:
        return [selection_dict[key] for key in selected]
    else:
        return []


def collect_families(doc=revit.doc):
    collector = DB.FilteredElementCollector(doc)
    collector.WhereElementIsNotElementType()
    collector.OfClass(clr.GetClrType(DB.Family))

    return collector.ToElements()


def select_families(doc=revit.doc):  # , multiselect=True):
    families = collect_families()

    selection_dict = OrderedDict()

    for family in families:
        key = "({}) {}".format(family.FamilyCategory.Name, family.Name)

        selection_dict[key] = family

    selected = forms.SelectFromList.show(
        sorted(selection_dict.keys()),
        multiselect=True
    )

    return [selection_dict[key] for key in selected]


def select_family_types(**kwargs):
    return select_of_class(
        DB.FamilySymbol, lambda x: "{0} - {1}".format(
            x.FamilyName,
            x.get_Parameter(DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        )
    )

    # fam_type_collector = DB.FilteredElementCollector(
    #      doc).WhereElementIsElementType().OfClass(DB.FamilySymbol)
    #  fam_types = fam_type_collector.ToElements()
    #
    #   fam_types_dict = OrderedDict()
    #
    #    # print(dir(fam_types[0]))
    #    # print(fam_types)
    #
    #    for fam_type in fam_types:
    #         symbol_name = fam_type.get_Parameter(
    #             DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
    #         family_name = fam_type.FamilyName
    #
    #         family_type_name = "{0} - {1}".format(family_name, symbol_name)
    #
    #         fam_types_dict[family_type_name] = fam_type
    #
    #     selected = forms.SelectFromList.show(
    #         sorted(fam_types_dict.keys()), multiselect=True)
    #
    #     if selected:
    #         return [fam_types_dict[key] for key in selected]
    #     else:
    #         return []


def select_detail_family_symbol(doc=revit.doc):
    collector = DB.FilteredElementCollector(doc)
    collector.WhereElementIsElementType()
    collector.OfClass(DB.FamilySymbol)
    elements = collector.ToElements()

    selection_dict = OrderedDict()

    for element in elements:
        key = "[{}] {}".format(
            element.Family.Name,
            element.get_Parameter(
                DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
            )
        selection_dict[key] = element

    selected = forms.SelectFromList.show(
        sorted(selection_dict.keys()),
    )

    return selection_dict[key]


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


def select_docs(multiselect=True, selection_filter=lambda x: True, **kwargs):
    docs = filter(selection_filter, revit.docs)

    doc_dict = {doc.Title: doc for doc in docs}

    selected = forms.SelectFromList.show(
        sorted(doc_dict.keys()),
        multiselect=multiselect,
        **kwargs
    )

    if multiselect:
        return [doc_dict[selected] for key in selected]
    else:
        return doc_dict[selected]


def select_filled_region(doc=revit.doc):
    """

    """
    collector = DB.FilteredElementCollector(doc)
    # collector.WhereElementIsElementType()
    collector.OfClass(DB.FilledRegionType)
    elements = collector.ToElements()

    selection_dict = OrderedDict()

    for element in elements:
        key = "{}".format(
            DB.Element.Name.GetValue(element)
            )
        selection_dict[key] = element

    selected = forms.SelectFromList.show(
        sorted(selection_dict.keys()),
    )

    return selection_dict[selected]
