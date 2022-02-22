from rpw import revit, DB
from pyrevit import script

# import clr
# clr.AddReference("System.Core")
# import System
# clr.ImportExtensions(System.Linq)

from collections import OrderedDict

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

def get_view_by_name(name, doc=revit.doc):
    collector = DB.FilteredElementCollector(doc)
    collector.OfClass(DB.View)
    collector.WhereElementIsNotElementType()

    collector.WherePasses(filter.view_name_filter(name))

    count = collector.GetElementCount()

    if count==1:
        return collector.FirstElement()
    else:
        logger.warning("More than one view found.")
        raise KeyError


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
    #collector.OfClass(DB.SpatialElement)
    collector.OfCategory(DB.BuiltInCategory.OST_Rooms)

    if phase_id:
        collector.WherePasses(filter.room_phase_filter(phase_id))

    return collector


def room_at_pt(rooms, pt):
    for room in rooms:
        if room.IsPointInRoom(pt):
            return room


def get_rooms_from_pt_list(pts, phase, view=revit.uidoc.ActiveView):
    # if not phase:
    #     phase_parameter = view.get_Parameter(DB.BuiltInParameter.VIEW_PHASE)
    #     phase_id = phase_parameter.AsElementId()

    rooms = room_collector(phase_id=phase.Id).ToElements()

    return [room_at_pt(rooms, pt) for pt in pts]
