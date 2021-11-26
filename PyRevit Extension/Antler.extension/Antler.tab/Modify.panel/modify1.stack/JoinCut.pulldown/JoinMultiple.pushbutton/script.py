from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script

from collections import OrderedDict
from System.Collections.Generic import List

from itertools import combinations


uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()

if uidoc.Selection.GetElementIds():
    elements = [doc.GetElement(id) for id in uidoc.Selection.GetElementIds()]
else:
    references = uidoc.Selection.PickObjects(
        UI.Selection.ObjectType.Element, "Select elements to be joined...")
    elements = [doc.GetElement(reference.ElementId)
                for reference in references]


if elements:
    with DB.Transaction(doc, __commandname__) as t:
        t.Start()
        for combination in combinations(elements, 2):
            try:
                DB.JoinGeometryUtils.JoinGeometry(
                    doc, combination[0], combination[1])
            except Exception as e:
                logger.warning("{}: {}".format(type(e), e))

        t.Commit()
