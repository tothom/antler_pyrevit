from rpw import revit, DB
from pyrevit import script, EXEC_PARAMS, forms
from System.Collections.Generic import List
import antler
from collections import OrderedDict

logger = script.get_logger()
output = script.get_output()


def transfer_element(element, doc):
    """"

    """
    assert element_type.Document != doc, "Target doc must be different than element doc."


def transfer_instance(instance, doc):
    """
    Copies an instance of any category to target document.
    """
    pass

def transfer_element_type(element_type, destination_doc):
    """
    Transfers element to target doc. Attempts to find similar element in
    target, and then ovveride properties, and if no element is found, simply
    copy the element.
    """
    assert element_type.Document != destination_doc, "Target doc must be different than element doc."

    # find_match
    match = antler.compare.find_similar_element(element_type, destination_doc)

    logger.debug(match)

    if match:
        diff = antler.compare.diff_elements(element_type, match)

    

    return

    with DB.Transaction(doc, "Push element") as t:
        t.Start()

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
                    List[DB.ElementId]([element_type.Id]),
                    doc,
                    DB.Transform.Identity,
                    DB.CopyPasteOptions()
                    )
            except Exception as e:
                logger.warning(e)
            else:
                logger.info("Element {element} copied to {doc}".format(
                    element=element_type,
                    doc=doc.Title
                ))

        t.Commit()


class LinkTransaction():
    """Creates a transaction on a linked document. Use with caution as it may
    take a long time to run. The link has to be unloaded, opened, modified,
    closed and then relinked."""

    def __init__(self, link, name=""):
        # Check if the link is a link?
        self.link = link
        self.name = name

    def __enter__(self):
        try:
            self.unload_link()
        except Exception as e:
            LOGGER.warning(e)
            raise e

        self.doc = self.open_link()

        self.transaction_group = DB.TransactionGroup(self.doc, self.name)

        return self.transaction_group

    def __exit__(self):
        # Check if everything is ok.
        # if self.doc.IsModifiable:
        #     pass

        # Error handling
        transaction_status = self.transaction_group.GetStatus()

        if transaction_status == DB.TransactionStatus.___:
            pass
        elif transaction_status == DB.TransactionStatus.___:
            pass
        else:
            pass

        self.close_link_doc()

        self.reload_link()

    def unload_link(self):
        pass

    def open_link(self):
        link_doc = link.Document
        path = link_doc.PathName

        # Try to not open any worksets to save loading time.
        workset_configuration = DB.WorksetConfiguration(DB.WorksetConfigurationOption.CloseAllWorksets)

        # Create new local with unique name?



        self self.cloud_model = link_doc.IsModelInCloud


    def close_link_doc(self):
        pass

    def reload_link(self):
        pass
