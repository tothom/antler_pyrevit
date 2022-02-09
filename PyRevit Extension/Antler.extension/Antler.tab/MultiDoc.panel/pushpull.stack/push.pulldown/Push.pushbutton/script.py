# -*- coding: utf-8 -*-

from rpw import revit, DB
from pyrevit import script, EXEC_PARAMS, forms
from System.Collections.Generic import List
import antler
from collections import OrderedDict


logger = script.get_logger()
output = script.get_output()


# select_elements_to_push
category = antler.forms.select_category(multiselect=False)

elements = antler.forms.select_types(categories=[category])

# select_docs_to_push_to
docs = antler.forms.select_docs(
    selection_filter=lambda x:not x.IsFamilyDocument and x != revit.doc)

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
            with DB.Transaction(doc, "Push element") as t:
                t.Start()

                match = antler.compare.find_similar_element(element, doc)

                logger.debug(match)

                if match:
                    diff = antler.compare.diff_elements(element, match)

                    logger.debug(diff)

                    for parameter, value in diff.items():
                        logger.info("Parameter {param} set from {old} to {new}".format(
                            param=parameter.Definition.Name,
                            old=antler.parameters.get_parameter_value(parameter),
                            new=value
                        ))

                        antler.parameters.set_parameter_value(parameter, value)


                    # override element parameters
                else:
                    pass
                    #copy element to doc
                t.Commit()
                # find_match

    tg.Assimilate()