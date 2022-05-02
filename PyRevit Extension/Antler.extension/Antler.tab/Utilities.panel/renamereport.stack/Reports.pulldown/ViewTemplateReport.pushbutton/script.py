# -*- coding: utf-8 -*-

from rpw import revit, DB, UI
from pyrevit import forms, script

import antler


collector = DB.FilteredElementCollector(revit.doc)
collector.OfClass(DB.View)
collector.WhereElementIsNotElementType()

views = collector.ToElements()

templates_dict = {}

for view in views:
    template = None
    addition = 0

    if view.IsTemplate:
        template = view
    elif view.ViewTemplateId:
        template = revit.doc.GetElement(view.ViewTemplateId)
        addition = 1

    if template:
        templates_dict.setdefault(template.Title, 0)
        templates_dict[template.Title] += addition

# print(templates_dict)

antler.util.print_dict_as_table(templates_dict, sort=True)
