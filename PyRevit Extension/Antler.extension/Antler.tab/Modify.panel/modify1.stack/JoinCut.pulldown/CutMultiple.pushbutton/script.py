from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script

from collections import OrderedDict
from System.Collections.Generic import List

__doc__ = "Cut multiple elements with one cutter"
__title__ = "Cut multiple"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()
output = script.get_output()


if uidoc.Selection.GetElementIds():
    elements = [doc.GetElement(id) for id in uidoc.Selection.GetElementIds()]
else:
    try:
        references = uidoc.Selection.PickObjects(
            UI.Selection.ObjectType.Element, "Select elements TO BE CUT...")
    except:
        script.exit()
    else:
        elements = [doc.GetElement(reference.ElementId)
                for reference in references]

cutter_references = uidoc.Selection.PickObjects(
    UI.Selection.ObjectType.Element, "Select CUTTERS...")

cutters = [doc.GetElement(a.ElementId) for a in cutter_references]


if elements:
    with DB.Transaction(doc, __title__) as t:
        t.Start()
        for element in elements:
            for cutter in cutters:
                try:
                    DB.InstanceVoidCutUtils.AddInstanceVoidCut(
                        doc, element, cutter)
                except Exception as e:
                    logger.warning("Cutting of {element} with {cutter} failed.".format(
                        element=output.linkify(element.Id),
                        cutter=output.linkify(cutter.Id),
                    ))
                    logger.warning(e)
        t.Commit()
