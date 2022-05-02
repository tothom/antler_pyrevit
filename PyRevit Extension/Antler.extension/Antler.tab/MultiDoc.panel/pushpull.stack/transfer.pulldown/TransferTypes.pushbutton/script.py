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


"""
Form - What do you want to transfer (and syncronize)?
    - Transfer types of current selection?
        - Yes or no?
        If no:
            Form:
            - Element Types?
                - Select Category
                - Select Element Types of Category
                - Match Element Types
                - Action: Transfer and override
            - View Templates
                - Select View Templates
                - Match View Templates
                - Action: Transfer and override
            - Sheets?
                - Transfer to other doc as placeholder sheets?
            - Views?
                -
            - Grids
                - Match Grids
            - Scope Boxes
                - Match Scope Boxes
            - Levels
                - Match Levels
            - Materials
                - Select Materials
                - Match Materials
                - Transfer Materials
                    - Materials, assets etc...
"""




# Select what to

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
            transfer.transfer_element(element, doc)

    tg.Assimilate()
