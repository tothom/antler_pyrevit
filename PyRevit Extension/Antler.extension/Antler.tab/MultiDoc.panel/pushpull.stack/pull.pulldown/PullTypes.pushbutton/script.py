# -*- coding: utf-8 -*-

from rpw import revit, DB
from pyrevit import script, EXEC_PARAMS, forms
from System.Collections.Generic import List
import antler
from collections import OrderedDict


logger = script.get_logger()
output = script.get_output()


other_doc = antler.forms.select_docs(
    multiselect=False, selection_filter=lambda x: not x.IsFamilyDocument or not x.IsLinked)

elements = antler.forms.select_types(doc=other_doc)

if not elements:
    script.exit()

this_doc = revit.doc

with DB.Transaction(this_doc, __commandname__) as t:
    t.Start()

    DB.ElementTransformUtils.CopyElements(
        other_doc,
        List[DB.ElementId](
            [element.Id for element in elements]),
        this_doc,
        DB.Transform.Identity,
        DB.CopyPasteOptions()
        )

    t.Commit()
