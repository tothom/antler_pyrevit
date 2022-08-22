# -*- coding: utf-8 -*-

from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script
from pyrevit import EXEC_PARAMS

# from collections import OrderedDict
#
# from Autodesk.Revit.Exceptions import InvalidOperationException

from System.Collections.Generic import List

import antler



logger = script.get_logger()
output = script.get_output()

other_doc = antler.forms.select_docs(
    multiselect=False, selection_filter=lambda x: not x.IsFamilyDocument)

logger.debug(other_doc.Title)

view_templates = antler.collectors.view_template_collector(doc=other_doc).ToElements()

logger.debug(view_templates)


selected_view_templates = antler.forms.select_elements(
        view_templates,
        naming_function=lambda x:x.Title,
        title="Select View Templates to pull into current model"
    ) or script.exit()

view_id_list = List[DB.ElementId]([view.Id for view in selected_view_templates])

with DB.Transaction(revit.doc, __commandname__) as t:
    t.Start()

    DB.ElementTransformUtils.CopyElements(
        other_doc,
        view_id_list,
        revit.doc,
        DB.Transform.Identity,
        DB.CopyPasteOptions()
        )

    t.Commit()
