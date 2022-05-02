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

strings = []

for element in elements:
    if isinstance(element, (DB.ViewSheet)):
        string = ("{number} - {name}".format(number=element.SheetNumber, name=element.Name))
    elif isinstance(element, DB.View):
        string = ("{name}".format(name=element.Name))
    else:
        string = ""

    print(string)

    strings.append(string)

# choice = forms.CommandSwitchWindow.show(
#         ["Copy to Clipboard"]
#     )
#
# logger.debug(choice)
#
# if choice:# == "Copy to Clipboard":
#     Clipboard.SetText('\r\n'.join(sheet_strings))
