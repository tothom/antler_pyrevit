from pyrevit import script

import antler_revit

output = script.get_output()

# print("Hallo!")


antler_revit.utils.close_revit(force_close=True)
