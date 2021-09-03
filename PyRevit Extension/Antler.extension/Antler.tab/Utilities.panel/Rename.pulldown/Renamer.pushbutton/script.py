from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

import antler.util

doc = revit.doc
uidoc = revit.uidoc

reference = uidoc.Selection.PickObject(UI.Selection.ObjectType.Element)
element = doc.GetElement(reference)

logger = script.get_logger()

# print("{element}".format(element=element))
# print("{parameters}".format(parameters=element.ParametersMap))

input_string = "{Comments} - {Mark}"

new_string = antler.util.string_from_template(element, input_string)

print(new_string)
