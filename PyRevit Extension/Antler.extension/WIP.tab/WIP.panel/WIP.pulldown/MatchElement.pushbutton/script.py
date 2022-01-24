# -*- coding: utf-8 -*-

# from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import script, forms
# from collections import OrderedDict

import antler

logger = script.get_logger()


ref = revit.uidoc.Selection.PickObject(
    UI.Selection.ObjectType.Element)

element = revit.doc.GetElement(ref)

other_doc = antler.forms.select_docs(multiselect=False)

matcher = antler.compare.ElementMatcher(element, other_doc)

logger.info(matcher.match)
