# -*- coding: utf-8 -*-

from rpw import revit, DB

from pyrevit import forms, script, EXEC_PARAMS

import sync
import antler

logger = script.get_logger()
output = script.get_output()

# unsaved_changes = any([
#     doc.IsModified for doc in revit.docs if not doc.IsWorkshared and not doc.IsLinked])

modified_docs = []

for doc in revit.docs:
    if not any((doc.IsWorkshared, doc.IsLinked)):
        if doc.IsModified:
            modified_docs.append(doc)

# modified_docs = [doc if doc.IsModified for doc in revit.docs

if modified_docs:
    forms.alert("You have unsaved changes. Please save or close these files and try again:\n\n{docs}".format(
        docs='\n'.join([doc.Title for doc in modified_docs])
    ))
    script.exit()
elif EXEC_PARAMS.config_mode:
    selected_option = forms.alert(
        "⚠ Warning!\n"
        "\n"
        "You are about to close Revit. This script does not check if there are "
        "unsaved changes in Dynamo. Please save any work in Dynamo before continuing.",
        options=["Continue", "Cancel"]
    ) or script.exit()

    if selected_option == "Cancel":
        script.exit()


relinquish_options = DB.RelinquishOptions(True)

transact_options = DB.TransactWithCentralOptions()
sync_options = DB.SynchronizeWithCentralOptions()
sync_options.SetRelinquishOptions(relinquish_options)

docs = [
    doc for doc in revit.docs if doc.IsWorkshared and not doc.IsLinked]

success = sync.sync_multiple_docs(
    docs, transact_options, sync_options, close_docs=True)

if success and EXEC_PARAMS.config_mode:
    antler.utils.close_revit()
