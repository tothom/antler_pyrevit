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

# select_titleblock
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


view = revit.uidoc.ActiveView


with DB.Transaction(revit.doc, __commandname__) as t:
    try:
        t.Start()

        new_sheet = DB.ViewSheet.Create(revit.doc, titleblock.Id)

        t.Commit()
    except Exception as e:
        logger.warning(e)
    else:
        revit.uidoc.ActiveView = new_sheet

        revit.uidoc.PromptToPlaceViewOnSheet(view, False)
