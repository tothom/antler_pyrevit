from rpw import revit, DB
from pyrevit import script
import clr

clr.AddReference("System.Core")
import System
clr.ImportExtensions(System.Linq)

# from collections import OrderedDict
import util
import filters

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


def elements_on_level_collector(level, doc=revit.doc):
    """
    """
    level_filter = DB.ElementLevelFilter(level.Id)
    collector = DB.FilteredElementCollector(doc)
    collector.WherePasses(level_filter)  # .ToElements()

    return collector


def revit_link_instances_collector(doc=revit.doc):
    collector = DB.FilteredElementCollector(doc)
    collector.OfClass(clr.GetClrType(DB.RevitLinkInstance))

    return collector

def revit_link_types_collector(doc=revit.doc):
    collector = DB.FilteredElementCollector(doc)
    collector.OfClass(clr.GetClrType(DB.RevitLinkType))

    return collector


def hosted_by_collector(host_element, doc=revit.doc):
    collector = DB.FilteredElementCollector(doc)
    collector.OfClass(DB.FamilyInstance)
    collector.WherePasses(filters.hosted_by_filter(host_element))

    return collector


def collect_instances_of_element_type(element_type):
    """
    Get instances by element type. Returns instances as elements, and not a collector.
    """
    collector = DB.FilteredElementCollector(element_type.Document)
    collector.WhereElementIsNotElementType()
    collector.OfCategory(util.builtin_category_from_category(element_type.Category))

    enumerable = collector.Where(lambda e: e.GetTypeId().IntegerValue.Equals(element_type.Id.IntegerValue))

    return enumerable.ToList()
