from rpw import revit, DB
from pyrevit import forms, script

import clr
from collections import OrderedDict
from System.Collections.Generic import List

import util, parameters
import collectors

from antler import LOGGER

"""
Contains all functions which generate UI forms in Antler.
"""

# LOGGER = script.get_LOGGER()


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

    LOGGER.debug(selected)

    if multiselect:
        return [categories_dict[a] for a in selected]
    else:
        return categories_dict.get(selected)

    # category_found = Revit.Elements.Category.ByName(str(category))


def select_elements(elements, naming_function=lambda x: x.Name, multiselect=True, sort_by_key=True, **kwargs):
    selection_dict = OrderedDict()

    LOGGER.debug(elements)

    # if not naming_function:
    #     def naming_function(x): return "{0}".format(x.Name)

    for element in elements:
        key = naming_function(element)
        selection_dict[key] = element

    if sort_by_key:
        selection_dict = OrderedDict(sorted(selection_dict.items()))

    keys = forms.SelectFromList.show(
        selection_dict.keys(),
        multiselect=multiselect,
        **kwargs
    )

    LOGGER.debug(dict(selection_dict))
    LOGGER.debug(keys)

    if multiselect:
        if keys:
            return [selection_dict[key] for key in keys]
        else:
            return []
    else:
        if keys:
            return selection_dict[keys]
        else:
            return None


def select_of_class(revit_class, naming_function, *args, **kwargs):
    elements = collectors.elements_of_class_collector(
        revit_class, *args, **kwargs).ToElements()

    selected_elements = select_elements(
        elements, naming_function, *args, **kwargs)

    return selected_elements


def select_of_category(category, naming_function, doc=revit.doc, *args, **kwargs):
    builtin_category = util.builtin_category_from_category(category)

    collector = DB.FilteredElementCollector(doc).OfCategory(builtin_category)
    collector.WhereElementIsElementType()

    elements = collector.ToElements()

    selected_elements = select_elements(
        elements, naming_function, *args, **kwargs)

    return selected_elements




def select_families(doc=revit.doc):  # , multiselect=True):
    families = collectors.family_collector().ToElements()
    return select_elements(families, lambda x: "({}) {}".format(x.FamilyCategory.Name, x.Name))



def select_family_types(**kwargs):
    return select_of_class(
        DB.FamilySymbol,
        lambda x: "{0} - {1}".format(
            x.FamilyName,
            x.get_Parameter(DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        )
    )



def select_detail_family_symbol(doc=revit.doc):
    elements = collectors.elements_of_class_collector(
        DB.FamilySymbol).ToElements()

    selected_elements = select_elements(elements, lambda x: "[{}] {}".format(
        x.Family.Name,
        x.get_Parameter(
            DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        ))

    return selected_elements


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

    # LOGGER.info(type_elements)

    selection_dict = {}

    for element in type_elements:
        LOGGER.debug(element)

        key_parts = []

        try:
            key_parts.append(element.Category.Name)
        except Exception as e:
            LOGGER.debug(e)
            # category_name = "No Category"

        try:
            key_parts.append(element.Family.Name)
        except Exception as e:
            LOGGER.debug(e)
            # family_name = "No Family"

        key_parts.append(DB.Element.Name.GetValue(element))

        key = ' - '.join(key_parts)

        # "{category_name} - {family_name} - {type_name}".format(
        #     category_name=category_name,
        #     family_name=family_name,
        #     type_name=type_name,
        #     )

        if key in selection_dict:
            LOGGER.warning("Key {} already in dict.".format(key))

        selection_dict[key] = element

    selected = forms.SelectFromList.show(
        sorted(selection_dict.keys()),
        multiselect=True
    )

    if not selected:
        return []

    return [selection_dict[key] for key in selected]


def select_worksets(doc=revit.doc, kind=DB.WorksetKind.UserWorkset, **kwargs):
    worksets = DB.FilteredWorksetCollector(doc).OfKind(kind).ToWorksets()

    return select_elements(worksets, **kwargs)


def select_levels(doc=revit.doc, *args, **kwargs):
    levels = DB.FilteredElementCollector(doc).OfCategory(
        DB.BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()

    levels = sorted(levels, key=lambda x:x.Elevation, reverse=True)

    LOGGER.debug([a.Elevation for a in levels])

    selected_elements = select_elements(levels, lambda level: "{} ({})".format(
        level.Name,
        DB.UnitFormatUtils.Format(
            doc.GetUnits(), DB.UnitType.UT_Length, level.Elevation, False, True)),
        sort_by_key=False,
        *args, **kwargs
        )

    return selected_elements

def select_parameters(element, *args, **kwargs):
    parameters = element.Parameters
