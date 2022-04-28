"""
"""
import clr
from System.Collections.Generic import List
from rpw import revit, DB, UI

from pyrevit import forms, script
import antler

from antler import LOGGER


views = forms.select_views(use_selection=True) or script.exit()

link_instances = antler.collectors.revit_link_instances_collector().ToElements()

LOGGER.debug(link_instances)

selected_link_instances = antler.forms.select_elements(link_instances,
	naming_function=lambda x:"{name}".format(
		name=x.Name
		)
	) or script.exit()


link_types = []

for link in selected_link_instances:
    link_type = clr.Convert(revit.doc.GetElement(link.GetTypeId()), DB.RevitLinkType)

    link_types.append(link_type)


with DB.Transaction(revit.doc, __commandname__) as t:
    t.Start()

    for view in views:
        for link_type in link_types:

            if link_type.IsHidden(view) and link_type.CanBeHidden(view):
                view.UnhideElements(List[DB.ElementId]([link_type.Id]))

    t.Commit()
