"""
"""
from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script

from collections import OrderedDict
from System.Collections.Generic import List

output = script.get_output()
logger = script.get_logger()

collector = DB.FilteredElementCollector(revit.doc)
collector.WhereElementIsNotElementType()
collector.OfClass(DB.View)

views = collector.ToElements()

latest_view = sorted(views, key=lambda x:x.Id.IntegerValue, reverse=True)[0]

try:
    revit.uidoc.ActiveView = latest_view
except Exception as e:
    output.resize(300, 300)
    logger.warning(e)
    output.self_destruct(3)
