# from __future__ import print_function

from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script

from collections import OrderedDict
from System.Collections.Generic import List

import re




__doc__ = "Select by by IFC GUID"
__title__ = "Select by IFC GUID"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc


def element_from_ifc_guid(guid_string):
    ifc_param = DB.BuiltInParameter.IFC_GUID

    pvp = DB.ParameterValueProvider(DB.ElementId(ifc_param))
    filter_rule = DB.FilterStringRule(
        pvp, DB.FilterStringContains(), guid_string, False)
    epf = DB.ElementParameterFilter(filter_rule)

    collector = DB.FilteredElementCollector(doc)
    collector.WherePasses(epf)

    # return collector.ToElements()

    return collector.FirstElement()


guids = forms.ask_for_string(
    prompt="Enter IFC GUID",
    title="IFC GUID"
)

# print(dir(forms))

if guids:
    elements = []
    output = script.get_output()

    for guid in re.split('[;,]', guids):
        guid = guid.strip()

        if guid == '':
            continue

        found = element_from_ifc_guid(guid)

        id = None

        if found:
            id = output.linkify(found.Id)
            elements.append(found)

        print("'{}': {}".format(guid, id))

    element_id_collection = List[DB.ElementId]()

    for element in elements:

        element_id_collection.Add(element.Id)

    # uidoc.Selection.SetElementIds(element_id_collection)
