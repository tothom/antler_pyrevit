# -*- coding: utf-8 -*-

from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

import antler

logger = script.get_logger()



# select_compound_classes
compound_classes = (
    DB.Floor,
    DB.RoofBase,
    DB.Wall,
    DB.Ceiling
)

filtered_elements = []

for id in revit.uidoc.Selection.GetElementIds():
    element = revit.doc.GetElement(id)

    category = element.Category

    if element.Category.Id.IntegerValue == DB.ElementId(DB.BuiltInCategory.OST_LegendComponents).IntegerValue:
        filtered_elements.append(element)

# OST_LegendComponents
logger.debug(filtered_elements)


with DB.TransactionGroup(revit.doc, __commandname__) as tg:
    tg.Start()

    for element in filtered_elements:
        parameter = element.get_Parameter(DB.BuiltInParameter.LEGEND_COMPONENT)

        component_type = revit.doc.GetElement(parameter.AsElementId())

        try:
            compound_structure = component_type.GetCompoundStructure()
        except Exception as e:
            continue

        bbox = element.get_BoundingBox(revit.uidoc.ActiveView)

        x = bbox.Min.X
        y = bbox.Max.Y
        line_length = bbox.Max.X - bbox.Min.X

        widths = []

        curve_array = DB.CurveArray()

        for layer in compound_structure.GetLayers():
            widths.append(layer.Width)

            start = DB.XYZ(x, y, 0)
            end = DB.XYZ(x+line_length, y, 0)

            logger.debug(start, end)

            line = DB.Line.CreateBound(start, end)

            curve_array.Append(line)

            y -= layer.Width

            material_id = layer.MaterialId
            material = revit.doc.GetElement(material_id)

            layer_string = ""

        with DB.Transaction(revit.doc, "Create Detail Curves") as t:
            t.Start()

            revit.doc.Create.NewDetailCurveArray(revit.uidoc.ActiveView, curve_array)

            t.Commit()




    tg.Assimilate()
