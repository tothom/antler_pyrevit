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

element_type = revit.doc.GetElement(element.GetTypeId())

other_doc = antler.forms.select_docs(multiselect=False)

other_element = antler.compare.find_similar_element(element_type, other_doc)

logger.info(other_element)
