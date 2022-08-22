"""
"""
from rpw import revit, DB
from pyrevit import forms, script
import antler

logger = script.get_logger()

views = forms.select_views() or script.exit()

if len(views) > 20:
    options = {
        "No, please stop!": False,
        "Sounds fine. Continue.": True
    }
    result = forms.alert(
        "You are about to open {} views. Are you sure?".format(len(views)),
        options=options.keys()
        )

    logger.debug(result)

    if not options.get(result, False):
        script.exit()

for view in views:
    revit.uidoc.ActiveView = view
