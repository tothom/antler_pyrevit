"""
"""

from rpw import revit, DB
from pyrevit import forms
from System.Collections.Generic import List

import antler.collectors

sheets = forms.select_sheets(use_selection=True)

element_ids = List[DB.ElementId]()

for sheet in sheets:
    titleblock_collector = antler.collectors.titleblocks_on_sheet_collector(sheet)

    element_ids.AddRange(titleblock_collector.ToElementIds())

revit.uidoc.Selection.SetElementIds(element_ids)
