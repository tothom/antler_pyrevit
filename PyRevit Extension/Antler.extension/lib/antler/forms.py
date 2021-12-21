from rpw import revit, DB
from pyrevit import forms, script

import clr
from collections import OrderedDict
from System.Collections.Generic import List

import util
import collectors

"""
Contains all functions which generate UI forms in Antler.
"""

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


def select_elements(elements, naming_function=lambda x: x.Name, multiselect=True, doc=revit.doc, **kwargs):
    selection_dict = OrderedDict()

    if not naming_function:
        def naming_function(x): return "{0}".format(x.Name)

    for element in elements:
        key = naming_function(element)
        selection_dict[key] = element

    selected = forms.SelectFromList.show(
        sorted(selection_dict.keys()),
        multiselect=multiselect,
        **kwargs
    )

    if multiselect:
        [selection_dict[key] for key in selected]
    else:
        return selection_dict[selected]


def select_of_class(revit_class, naming_function, *args, **kwargs):
    elements = collectors.elements_of_class_collector(
        revit_class, *args, **kwargs).ToElements()

    selected_elements = select_elements(
        elements, naming_function, *args, **kwargs)

    return selected_elements

    # selection_dict = OrderedDict()
    #
    # if not naming_function:
    #     def naming_function(x): return "{0}".format(x.Name)
    #
    # for element in elements:
    #     key = naming_function(element)
    #     selection_dict[key] = element
    #
    # selected = forms.SelectFromList.show(
    #     sorted(selection_dict.keys()),
    #     multiselect=multiselect,
    #     **kwargs
    # )
    #
    # if selected:
    #     return [selection_dict[key] for key in selected]
    # else:
    #     return []


def select_families(doc=revit.doc):  # , multiselect=True):
    families = collectors.family_collector().ToElements()
    return select_elements(families, lambda x: "({}) {}".format(x.FamilyCategory.Name, x.Name))

    # selection_dict = OrderedDict()
    #
    # for family in families:
    #     key = "({}) {}".format(family.FamilyCategory.Name, family.Name)
    #
    #     selection_dict[key] = family
    #
    # selected = forms.SelectFromList.show(
    #     sorted(selection_dict.keys()),
    #     multiselect=True
    # )
    #
    # return [selection_dict[key] for key in selected]


def select_family_types(**kwargs):
    return select_of_class(
        DB.FamilySymbol,
        lambda x: "{0} - {1}".format(
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
    elements = collectors.elements_of_class_collector(
        DB.FamilySymbol).ToElements

    selected_elements = select_elements(elements, lambda x: "[{}] {}".format(
        x.Family.Name,
        x.get_Parameter(
            DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        ))

    return selected_elements

    # selection_dict = OrderedDict()
    #
    # for element in elements:
    #     key = "[{}] {}".format(
    #         element.Family.Name,
    #         element.get_Parameter(
    #             DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
    #         )
    #     selection_dict[key] = element
    #
    # selected = forms.SelectFromList.show(
    #     sorted(selection_dict.keys()),
    # )
    #
    # return selection_dict[key]


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


def select_docs(multiselect=True, selection_filter=lambda x: True, **kwargs):
    docs = filter(selection_filter, revit.docs)

    doc_dict = {doc.Title: doc for doc in docs}

    selected = forms.SelectFromList.show(
        sorted(doc_dict.keys()),
        multiselect=multiselect,
        **kwargs
    )

    if multiselect:
        selected = selected or []
        return [doc_dict[key] for key in selected]
    else:
        # selected
        return doc_dict.get(selected)


def select_types(categories=[], doc=revit.doc):
    collector = DB.FilteredElementCollector(doc).WhereElementIsElementType()

    if categories:
        category_list = List[DB.ElementId](c.Id for c in categories)
        multi_category_filter = DB.ElementMulticategoryFilter(category_list)

        collector.WherePasses(multi_category_filter)

    type_elements = collector.ToElements()

    logger.info(type_elements)

    selection_dict = {}

    for element in type_elements:
        try:
            category_name = DB.Category.Name
        except Exception as e:
            logger.info(e)
            category_name = "No Category"

        try:
            family_name = element.Family.Name
        except Exception as e:
            logger.info(e)
            family_name = "No Family"

        type_name = DB.Element.Name.GetValue(element)

        selection_dict[
            "{category_name} - {family_name} - {type_name}".format(
                category_name=category_name,
                family_name=family_name,
                type_name=type_name,
                )
            ] = element

    selected = forms.SelectFromList.show(
        sorted(selection_dict.keys()),
        multiselect=True
    )

    if not selected:
        return []

    return [selection_dict[key] for key in selected]
