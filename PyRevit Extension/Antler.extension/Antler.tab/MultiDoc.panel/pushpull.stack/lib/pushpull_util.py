from rpw import revit, DB
from pyrevit import script, EXEC_PARAMS, forms
from System.Collections.Generic import List
import antler
from collections import OrderedDict

logger = script.get_logger()
output = script.get_output()


def transfer_element(element, doc):
    """
    Transfers element to target doc. Attempts to find similar element in
    target, and then ovveride properties, and if no element is found, simply
    copy the element.
    """
    assert element.Document != doc, "Target doc must be different than element doc."

    with DB.Transaction(doc, "Push element") as t:
        t.Start()

        # find_match
        match = antler.compare.find_similar_element(element, doc)

        logger.debug(match)

        if match:
            diff = antler.compare.diff_elements(element, match)

            logger.debug(diff)
            # override element parameters

            for parameter, value in diff.items():
                antler.parameters.set_parameter_value(parameter, value)

                logger.info("Parameter {param} set from {old} to {new}".format(
                    param=parameter.Definition.Name,
                    old=antler.parameters.get_parameter_value(
                        parameter),
                    new=value
                ))
        else:
            # copy element to doc
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
