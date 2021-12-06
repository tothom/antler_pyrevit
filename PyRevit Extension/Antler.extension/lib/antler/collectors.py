from rpw import revit, DB
from pyrevit import script
import clr
# from collections import OrderedDict
# import util

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
