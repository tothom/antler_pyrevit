# -*- coding: utf-8 -*-

from rpw import revit, DB
from pyrevit import script, EXEC_PARAMS, forms
from System.Collections.Generic import List
import antler
from collections import OrderedDict

import transfer

logger = script.get_logger()
output = script.get_output()

# Form - Transfer to this model or transfer from this model?
# Should be two buttons...

if EXEC_PARAMS.config_mode:
    # Pull elements from other doc to this doc
    pass
else:
    # Push elements from this doc to other doc
    pass




project_parameters = antler.forms.select_project_parameters()

script.exit()
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
            transfer.transfer_element(element, doc)

    tg.Assimilate()
