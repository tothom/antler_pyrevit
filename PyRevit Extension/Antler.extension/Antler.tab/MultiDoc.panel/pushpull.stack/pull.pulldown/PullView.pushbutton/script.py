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

views = forms.select_views(
        title="Select Views to pull into current model",
        doc=other_doc
    )

view_id_list = List[DB.ElementId]()
[view_id_list.Add(view.Id) for view in views]

if views:
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
