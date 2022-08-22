# -*- coding: utf-8 -*-

from rpw import revit, DB, UI

from pyrevit import forms, script
# from pyrevit import EXEC_PARAMS

# from collections import OrderedDict

from Autodesk.Revit.Exceptions import InvalidOperationException

import time

logger = script.get_logger()
output = script.get_output()



def sync_multiple_docs(docs, transact_options, sync_options, close_docs=False, close_revit=False):
    """
    Super simple function to sync multiple docs with central. Does not give any
    feedback at all on how a sync fails, if it fails. Instead the function just
    continues with next. However, on failure, the function will return False.
    """
    if not docs:
        return True

    t_start = time.time()

    print("Synchronising {0} docs...".format(len(docs)))
    output.indeterminate_progress(True)

    success = True

    for i, doc in enumerate(docs):
        print("Trying to synchronize {0}...".format(doc.Title))

        t0 = time.time()

        try:
            doc.SynchronizeWithCentral(transact_options, sync_options)
        except Exception as e:
            logger.warning("Document NOT synchronized!")
            logger.debug(type(e), e)
            success = False
        else:
            print("Document synchronized!")
            if close_docs:
                try:
                    print("Trying to close document.")
                    doc.Close()
                except InvalidOperationException as e:
                    close_doc = UI.RevitCommandId.LookupPostableCommandId(
                        UI.PostableCommand.Close)
                    revit.uiapp.PostCommand(close_doc)
                else:
                    print("Document closed.")

            #     logger.warning(e.Message)

        t1 = time.time()

        print("Process took {:.3g}s.".format(t1-t0))

        output.indeterminate_progress(False)
        output.update_progress(i + 1, len(docs))

    t_end = time.time()

    print("Done in {:.3g} s! 👍".format(t_end - t_start))

    return success
