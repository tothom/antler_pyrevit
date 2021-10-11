# -*- coding: utf-8 -*-

import antler
from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

from System.Collections.Generic import List

logger = script.get_logger()

elements = List[DB.ElementId]()
[elements.Add(a.Id) for a in antler.util.preselect()]

# if not elements:
#     script.exit()

docs = antler.ui.select_docs()

copy_paste_options = DB.CopyPasteOptions()


for destination_doc in docs:

    # Unload doc, maybe not necessary because revit may do it automatically
    # when opening the link.

    # Open doc

    # Copy elements

    # Close doc

    # Reload doc

    # with DB.Transaction(destination_doc, __commandname__) as t:
    #     t.Start()

    DB.ElementTransformUtils.CopyElements(
        revit.doc,
        elements,
        destination_doc,
        None,
        copy_paste_options
        )

    # t.Commit()
