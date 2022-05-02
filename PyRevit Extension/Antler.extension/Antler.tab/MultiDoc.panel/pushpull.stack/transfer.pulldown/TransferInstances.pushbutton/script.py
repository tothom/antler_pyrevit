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

"""




# Select what to

elements = antler.ui.preselect()

# if selection:
# elements = [revit.doc.GetElement(ref) for ref in selection]
# elements = list(set(elements))


# select_docs_to_push_to
docs = antler.forms.select_docs(
    selection_filter=lambda x: not x.IsFamilyDocument and x != revit.doc) or script.exit()

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
            with DB.Transaction(doc, "Transfer instances") as t:
                t.Start()
                try:
                    DB.ElementTransformUtils.CopyElements(
                        revit.doc,
                        List[DB.ElementId]([element.Id]),
                        doc,
                        DB.Transform.Identity,
                        DB.CopyPasteOptions()
                        )
                except Exception as e:
                    logger.warning(e)
                else:
                    logger.info("Element {element} copied to {doc}".format(
                        element=element,
                        doc=doc.Title
                    ))
                t.Commit()

    tg.Assimilate()
