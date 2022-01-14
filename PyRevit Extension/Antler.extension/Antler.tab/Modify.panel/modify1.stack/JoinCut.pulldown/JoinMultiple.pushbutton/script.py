from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script

from collections import OrderedDict
from System.Collections.Generic import List

from itertools import combinations


uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()
output = script.get_output()

if uidoc.Selection.GetElementIds():
    elements = [doc.GetElement(id) for id in uidoc.Selection.GetElementIds()]
else:
    references = uidoc.Selection.PickObjects(
        UI.Selection.ObjectType.Element, "Select elements to be joined...")
    elements = [doc.GetElement(reference.ElementId)
                for reference in references]


if elements:
    # output.indeterminate_progress(True)
    element_combinations = combinations(elements, 2)
    length = sum(1 for _ in combinations(elements, 2))
    i = 1

    with DB.Transaction(doc, __commandname__) as t:
        t.Start()

        for combination in combinations(elements, 2):
            try:
                DB.JoinGeometryUtils.JoinGeometry(
                    doc, combination[0], combination[1])
            except Exception as e:
                logger.debug("{}: {}".format(type(e), e))
            # else:
            #     logger.info("{a} and {b} succesfully joined.".format(
            #         a=combination[0],
            #         b=combination[1],
            #         # a=output.linkify(combination[0].Id),
            #         # b=output.linkify(combination[1].Id),
            #         )
            #     )

            # output.indeterminate_progress(False)
            output.update_progress(i, length)
            i += 1

        t.Commit()
