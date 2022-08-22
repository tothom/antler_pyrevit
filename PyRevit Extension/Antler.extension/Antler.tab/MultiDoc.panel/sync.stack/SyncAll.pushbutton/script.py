# -*- coding: utf-8 -*-

# from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script
from pyrevit import EXEC_PARAMS

from collections import OrderedDict

from Autodesk.Revit.Exceptions import InvalidOperationException

import time
import sync

import antler_revit

logger = script.get_logger()
output = script.get_output()

relinquish_options = DB.RelinquishOptions(EXEC_PARAMS.config_mode)

# options = OrderedDict()
#
# options["Elements checked out by the current user should be relinquished."] = 'CheckedOutElements'
# options["Family worksets owned by the current user should be relinquished."] = 'FamilyWorksets'
# options["Project standards worksets owned by the current user should be relinquished."] = 'StandardWorksets'
# options["User-created worksets owned by the current user should be relinquished."] = 'UserWorksets'
# options["View worksets owned by the current user should be relinquished."] = 'ViewWorksets'
#
#
# selected = forms.SelectFromList.show(
#     options.keys(),
#     title="Select relinquish options",
#     multiselect=True
# )# or script.exit()
#
# logger.debug(selected)
#
# if selected is None:
#     script.exit()
#
# for a in selected:
#     setattr(relinquish_options, options[a], True)

transact_options = DB.TransactWithCentralOptions()
sync_options = DB.SynchronizeWithCentralOptions()
sync_options.SetRelinquishOptions(relinquish_options)

# print(
# 	sync_options.RelinquishBorrowedElements,
# 	sync_options.RelinquishFamilyWorksets,
# 	sync_options.RelinquishProjectStandardWorksets,
# 	sync_options.RelinquishUserCreatedWorksets,
# 	sync_options.RelinquishViewWorksets,
# 	sync_options.SaveLocalAfter,
# 	sync_options.SaveLocalBefore,
# 	sync_options.SaveLocalFile
# 	)

#print("Syncing and relinquishing all workshared docs. Enjoy your lunch!")

docs = [
    doc for doc in revit.docs if doc.IsWorkshared and not doc.IsLinked]

sync.sync_multiple_docs(docs, transact_options, sync_options, close_docs=False)

# output.self_destruct(20)

# antler_revit.utils.close_revit()
