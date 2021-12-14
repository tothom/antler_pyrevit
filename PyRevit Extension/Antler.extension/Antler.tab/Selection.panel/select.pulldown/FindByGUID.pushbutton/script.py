# from __future__ import print_function
from rpw import revit, DB, UI
from pyrevit import forms, script
from System.Collections.Generic import List
import re

import antler.filters

logger = script.get_logger()

def element_from_ifc_guid(guid, doc=revit.doc):
    collector = DB.FilteredElementCollector(doc)
    collector.WherePasses(antler.filters.ifc_guid_filter(guid))

    count = collector.GetElementCount()

    if count > 1:
        logger.warning("GUID '{guid}' correspondes to more than one element.".format(guid=guid))
    # return collector.ToElements()

    return collector.FirstElement()


guids = forms.ask_for_string(
    prompt="Enter IFC GUIDs, separated by , ; or space",
    title="IFC GUID"
)

# print(dir(forms))

if guids:
    elements = []

    output = script.get_output()

    for guid in re.split('[;, ]', guids):
        guid = guid.strip()

        if guid:
            found_element = element_from_ifc_guid(guid)

            id = None

            if found_element:
                id = output.linkify(found_element.Id)
                elements.append(found_element)

            print("'{}': {}".format(guid, id))

    if elements:
        element_id_collection = List[DB.ElementId]()

        for element in elements:
            element_id_collection.Add(element.Id)

        revit.uidoc.Selection.SetElementIds(element_id_collection)
