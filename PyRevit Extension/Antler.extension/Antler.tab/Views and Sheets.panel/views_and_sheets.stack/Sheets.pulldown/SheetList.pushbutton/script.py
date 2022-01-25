# from System.Collections.Generic import *
# from rpw import revit, DB, UI

from pyrevit import forms, script

output = script.get_output()

# Select Sheets
sheets = forms.select_sheets(use_selection=True)

for sheet in sheets:
    output.print_md("**{number}** - {name}".format(number=sheet.SheetNumber, name=sheet.Name))
