from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms

import sheets

__doc__ = "Duplicates selected Sheets"
__title__ = "Duplicate Sheets"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc



# Select Sheets
sheets = forms.select_sheets(use_selection=True)

options = {
 	"Duplicate view": DB.ViewDuplicateOption.Duplicate,
 	"Duplicate as Dependent": DB.ViewDuplicateOption.AsDependent,
 	"Duplicate with Detailing" : DB.ViewDuplicateOption.WithDetailing
}

selected_option = forms.CommandSwitchWindow.show(
    options.keys(),
    message='Duplicate option'
)

option = options[selected_option]


if sheets:
    tg = DB.TransactionGroup(doc, __title__)
    tg.Start()

    sheets_new = []

    for sheet in sheets:
        sheet_new = sheets.duplicate_sheet(sheet, duplicate_option=option)
        uidoc.ActiveView = sheet_new

    tg.Assimilate()
