"""
"""

from rpw import revit, DB#, UI

from pyrevit import forms, script

import antler.forms

logger = script.get_logger()




# Don't bother if view is already a sheet.
if isinstance(revit.uidoc.ActiveView, DB.ViewSheet):
    script.exit()
# elif 


collector = DB.FilteredElementCollector(revit.doc)
collector.OfCategory(DB.BuiltInCategory.OST_TitleBlocks)
collector.WhereElementIsElementType()


titleblock_types = collector.ToElements()


titleblock = antler.forms.select_elements(
    titleblock_types, multiselect=False,
    naming_function=lambda x:'{} : {}'.format(
        x.FamilyName, x.get_Parameter(
            DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString())
    ) or script.exit()





with DB.Transaction(revit.doc, __commandname__) as t:
    try:
        t.Start()
        new_sheet = DB.ViewSheet.Create(revit.doc, titleblock.Id)

        viewport = DB.Viewport.Create(revit.doc, new_sheet.Id, revit.doc.ActiveView.Id, DB.XYZ(0,0,0))
        t.Commit()
    except Exception as e:
        logger.warning(e)
    else:
        revit.uidoc.ActiveView = new_sheet
