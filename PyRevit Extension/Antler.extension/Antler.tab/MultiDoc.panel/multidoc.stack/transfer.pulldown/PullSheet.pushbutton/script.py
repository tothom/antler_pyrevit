from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms

import antler


other_doc = antler.forms.select_docs(multiselect=False) or script.exit()

# Select Sheets
sheets = forms.select_sheets(
    use_selection=True, doc=other_doc) or script.exit()
#
# options = {
#  	"Duplicate view": DB.ViewDuplicateOption.Duplicate,
#  	"Duplicate as Dependent": DB.ViewDuplicateOption.AsDependent,
#  	"Duplicate with Detailing" : DB.ViewDuplicateOption.WithDetailing
# }
#
# selected_option = forms.CommandSwitchWindow.show(
#     options.keys(),
#     message='Duplicate option'
# )
#
# option = options[selected_option]
#
#
if sheets:
    tg = DB.TransactionGroup(revit.doc, __commandname__)
    tg.Start()

    sheets_new = []

    for sheet in sheets:
        sheet_new = antler.views.duplicate_sheet(
            sheet, destination_doc=revit.doc)
        #uidoc.ActiveView = sheet_new

    tg.Assimilate()
