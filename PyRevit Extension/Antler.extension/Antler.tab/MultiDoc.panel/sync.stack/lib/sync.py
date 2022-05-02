# -*- coding: utf-8 -*-

from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script
from pyrevit import EXEC_PARAMS

from collections import OrderedDict

from Autodesk.Revit.Exceptions import InvalidOperationException

import time

logger = script.get_logger()
output = script.get_output()

def sync_multiple_docs(docs, transact_options, sync_options, close_docs=False):
    t_start = time.time()

    print("Synchronising {0} docs...".format(len(docs)))
    output.indeterminate_progress(True)

    for i, doc in enumerate(docs):
        print("Trying to synchronize {0}...".format(doc.Title))

        t0 = time.time()

        try:
            doc.SynchronizeWithCentral(transact_options, sync_options)
            print("Document synchronized!")
        except Exception as e:
            logger.warning("Document NOT synchronized!")
            logger.debug(type(e), e)
        else:
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
