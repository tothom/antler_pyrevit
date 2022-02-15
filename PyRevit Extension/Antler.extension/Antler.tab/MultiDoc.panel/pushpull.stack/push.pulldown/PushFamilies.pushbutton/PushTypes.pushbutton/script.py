# -*- coding: utf-8 -*-

from rpw import revit, DB
from pyrevit import script, EXEC_PARAMS, forms
from System.Collections.Generic import List
import antler
from collections import OrderedDict

import pushpull_util

logger = script.get_logger()
output = script.get_output()


selection = antler.ui.preselect()

if selection:
    elements = [revit.doc.GetElement(element.GetTypeId()) for element in selection]
    elements = list(set(elements))
else:
    # select_elements_to_push
    category = antler.forms.select_category(multiselect=False) or script.exit()
    elements = antler.forms.select_types(categories=[category]) or script.exit()

# select_docs_to_push_to
docs = antler.forms.select_docs(
    selection_filter=lambda x: not x.IsFamilyDocument and x != revit.doc and not x.IsLinked) or script.exit()

logger.debug(docs)

# relations = [
#     # {'doc_id_01': 'element_id_01', 'doc_id_02': 'element_id_02',}
# ]
#
# match_methods = {
#     'By Element Name': None,
#     'By Parameter': None,
#     'By Relation Database': None,
# }

# transaction_group
with DB.TransactionGroup(revit.doc, __commandname__) as tg:
    tg.Start()

    for element in elements:
        for doc in docs:
            pushpull_util.push_element_to_doc(element, doc)

    tg.Assimilate()
