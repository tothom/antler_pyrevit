from rpw import revit, DB, UI

doc = revit.doc
uidoc = revit.uidoc

reference = uidoc.Selection.PickObject(UI.Selection.ObjectType.Element)
element = doc.GetElement(reference)

print("{element}".format(element=element))
