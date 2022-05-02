# -*- coding: utf-8 -*-

# from System.Collections.Generic import *
from rpw import revit, DB, UI
from pyrevit import forms, script
import antler

logger = script.get_logger()

name = forms.ask_for_string(
	prompt="Enter View name to search for",
	title="View name"
	)

view = antler.collectors.get_view_by_name(name)

logger.debug(view.Title)

revit.uidoc.ActiveView = view
