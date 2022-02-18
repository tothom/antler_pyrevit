# from System.Collections.Generic import *
from rpw import revit, DB

from pyrevit import script
# from pyrevit import forms

from System.Windows import Clipboard


output = script.get_output()
logger = script.get_logger()

# Select Sheets
# sheets = forms.select_sheets(use_selection=True)

elements = [revit.doc.GetElement(id) for id in revit.uidoc.Selection.GetElementIds()]

sheet_strings = []

for element in elements:
    if isinstance(element, (DB.ViewSheet)):
        sheet_string = ("{number} - {name}".format(number=element.SheetNumber, name=element.Name))

        print(sheet_string)

        sheet_strings.append(sheet_string)

# choice = forms.CommandSwitchWindow.show(
#         ["Copy to Clipboard"]
#     )
#
# logger.debug(choice)
#
# if choice:# == "Copy to Clipboard":
#     Clipboard.SetText('\r\n'.join(sheet_strings))
