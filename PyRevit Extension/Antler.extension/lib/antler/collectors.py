import filters
import utils
from collections import OrderedDict

from rpw import revit, DB
from pyrevit import script

import clr

# clr.AddReference("System.Core")
import System.Linq
clr.ImportExtensions(System.Linq)


logger = script.get_logger()


def family_collector(doc=revit.doc):
    collector = DB.FilteredElementCollector(doc)
    collector.WhereElementIsNotElementType()
    collector.OfClass(clr.GetClrType(DB.Family))

    return collector


def elements_of_class_collector(revit_class, select_types=True, doc=revit.doc, **kwargs):
    collector = DB.FilteredElementCollector(doc)

    if select_types:
        collector.WhereElementIsElementType()
    else:
        collector.WhereElementIsNotElementType()

    collector.OfClass(revit_class)

    return collector


# def


def elements_on_level_collector(level, doc=revit.doc):
    """
    """
    level_filter = DB.ElementLevelFilter(level.Id)
    collector = DB.FilteredElementCollector(doc)
    collector.WherePasses(level_filter)  # .ToElements()

    return collector


def revit_link_instances_collector(doc=revit.doc):
    collector = DB.FilteredElementCollector(doc)
    # collector.OfCategory(DB.BuiltInCategory.OST_RvtLinks)
    collector.OfClass(clr.GetClrType(DB.RevitLinkInstance))

    return collector


def revit_link_types_collector(doc=revit.doc):
    collector = DB.FilteredElementCollector(doc)
    # collector.OfCategory(DB.BuiltInCategory.OST_RvtLinks)
    collector.OfClass(clr.GetClrType(DB.RevitLinkType))

    return collector


def hosted_by_collector(host_element, doc=revit.doc):
    collector = DB.FilteredElementCollector(doc)
    collector.OfClass(DB.FamilyInstance)
    collector.WherePasses(filters.hosted_by_filter(host_element))

    return collector


def get_instances_of_element_type(element_type):
    """
    Get instances by element type. Returns instances as elements, and not a collector.
    """
    collector = DB.FilteredElementCollector(element_type.Document)
    collector.WhereElementIsNotElementType()
    collector.OfCategoryId(element_type.Category.Id)

    # collector.Where(lambda e: e.GetTypeId().IntegerValue == element_type.Id.IntegerValue)

    enumerable = collector.ToElements().Where(
        lambda e: e.GetTypeId().IntegerValue == element_type.Id.IntegerValue)

    return enumerable.ToList()


def instances_of_element_type_collector(element_type):
    """
    Get instances by element type. Returns a FilteredElementCollector with
    these instances already filtered.
    """
    collector = DB.FilteredElementCollector(element_type.Document)
    collector.WhereElementIsNotElementType()
    collector.OfCategoryId(element_type.Category.Id)

    collector.WherePasses(DB.FamilyInstanceFilter(element_type.Document, element_type.Id))

    return collector


def symbols_of_family_collector(family):
    """
    Get collector with symbols (family types) of input family.
    """
    collector = DB.FilteredElementCollector(family.Document)
    collector.WherePasses(DB.FamilySymbolFilter(family.Id))

    return collector


def view_template_collector(doc=revit.doc):
    collector = DB.FilteredElementCollector(doc)
    collector.OfClass(DB.View)
    collector.WhereElementIsNotElementType()

    # enumerable = collector.Where(lambda x: x.IsTemplate)
    collector.Where(lambda x: x.IsTemplate)

    return collector


def collect_view_templates(doc=revit.doc):
    collector = DB.FilteredElementCollector(doc)
    collector.OfClass(DB.View)
    collector.WhereElementIsNotElementType()
    # collector.WhereElementIsNotElementType()

    # is_view_template = lambda x: x.IsTemplate

    elements = collector.ToElements()

    elements = [a for a in elements if a.IsTemplate]

    # collector.WherePasses(lambda x: x.IsTemplate)
    #
    # logger.info(collector)

    return elements


def room_collector(doc=revit.doc, phase_id=None):
    collector = DB.FilteredElementCollector(doc).WhereElementIsNotElementType()
    collector.OfCategory(DB.BuiltInCategory.OST_Rooms)

    if phase_id:
        collector.WherePasses(filters.room_phase_filter(phase_id))

    return collector


def collect_project_parameters(doc=revit.doc):
    parameter_bindings_dict = {}

    iterator = doc.ParameterBindings.ForwardIterator()
    iterator.Reset()

    while iterator.MoveNext():
        parameter_bindings_dict[iterator.Key] = iterator.Current

    return parameter_bindings_dict


def area_schemes_collector(doc=revit.doc):
    collector = DB.FilteredElementCollector(doc)
    collector.OfClass(DB.AreaScheme)

    return collector


def areas_of_area_scheme_collector(area_scheme):
    doc = area_scheme.Document

    collector = DB.FilteredElementCollector(doc)
    collector.OfClass(DB.Area).WhereElementIsNotElementType()

    provider = DB.ParameterValueProvider(
        DB.ElementId(DB.BuiltInParameter.AREA_SCHEME_ID))
    rule = DB.FilterElementIdRule(
        provider, DB.FilterNumericEquals(), area_scheme.Id)
    parameter_filter = DB.ElementParameterFilter(rule)

    collector.WherePasses(parameter_filter)

    return collector


def titleblocks_on_sheet_collector(sheet):
    """
    Returns all Titleblocks on Sheet
    """
    collector = DB.FilteredElementCollector(
        sheet.Document).OwnedByView(sheet.Id)
    collector.OfCategory(DB.BuiltInCategory.OST_TitleBlocks)

    return collector


def collect_materials(doc=revit.doc):
    collector = DB.FilteredElementCollector(doc)
    collector.OfClass(clr.GetClrType(DB.Material))
    collector.Cast[DB.Material]

    return collector

# ############
# Get or search for some Element by name or other parameter
# ############

def get_view_by_name(name, doc=revit.doc):
    collector = DB.FilteredElementCollector(doc)
    collector.OfClass(DB.View)
    collector.WhereElementIsNotElementType()

    collector.WherePasses(filter.view_name_filter(name))

    count = collector.GetElementCount()

    if count == 1:
        return collector.FirstElement()
    else:
        logger.warning("More than one view found.")
        raise KeyError


def get_sheet_by_number(sheet_number):
    provider = DB.ParameterValueProvider(
        DB.ElementId(DB.BuiltInParameter.SHEET_NUMBER))
    rule = DB.FilterStringRule(
        provider, DB.FilterStringEquals(), sheet_number, False)
    parameter_filter = DB.ElementParameterFilter(rule)

    collector = DB.FilteredElementCollector(revit.doc)
    collector.OfCategory(DB.BuiltInCategory.OST_Sheets)

    collector.WherePasses(parameter_filter)

    # logger.debug(collector.GetElementCount())

    return collector.FirstElement()


def get_doc_by_name(doc_name, filter_func=lambda x: True):
    for doc in revit.docs:
        if filter_func(doc) and doc.Title == doc_name:
            return doc


def get_material_by_name(material_name, doc):
    collector = material_collector(doc)

    enumerable = collector.Where(lambda x: x.Name == material_name)

    LOGGER.debug(enumerable.Count())

    if not enumerable.Empty():
        return enumerable.First()


def get_element_by_name(name, hint=None, doc=revit.doc):
    pass

def get_family_type_by_name(name, doc=revit.doc):
    return None