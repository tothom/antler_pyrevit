# -*- coding: utf-8 -*-

from rpw import revit, DB

from pyrevit import forms, script

import sync

logger = script.get_logger()
output = script.get_output()

relinquish_options = DB.RelinquishOptions(True)

transact_options = DB.TransactWithCentralOptions()
sync_options = DB.SynchronizeWithCentralOptions()
sync_options.SetRelinquishOptions(relinquish_options)

docs = [
    doc for doc in revit.docs if doc.IsWorkshared and not doc.IsLinked]

print("Syncing and relinquishing all workshared docs. Enjoy your lunch!")

sync.sync_multiple_docs(docs, transact_options, sync_options, close_docs=False)

output.self_destruct(20)
