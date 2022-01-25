# -*- coding: utf-8 -*-

from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

from collections import OrderedDict

import antler

logger = script.get_logger()
output = script.get_output()

selection = revit.uidoc.Selection.GetElementIds() or revit.uidoc.Selection.PickObjects(
    UI.Selection.ObjectType.Element, "Select objects to snoop.")

elements = [revit.doc.GetElement(id) for id in selection]

snoop_dict_list = []

attributes = [
    'Creator', 'LastChangedBy', 'Owner'
]

for element in elements:
    worksharing_tooltip_info = DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc,
                                                              element.Id)
    # logger.info(dir(worksharing_tooltip_info))

    snoop_dict = OrderedDict()

    snoop_dict = {'ElementId': output.linkify(element.Id)}
    snoop_dict.update({attr: getattr(worksharing_tooltip_info, attr) for attr in attributes})

    snoop_dict_list.append(snoop_dict)

antler.util.print_dict_list(snoop_dict_list, columns=['ElementId']+attributes)
