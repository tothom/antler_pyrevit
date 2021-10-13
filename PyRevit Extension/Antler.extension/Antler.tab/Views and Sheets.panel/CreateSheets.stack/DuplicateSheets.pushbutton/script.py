from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms

__doc__ = "Duplicates selected Sheets"
__title__ = "Duplicate Sheets"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

def titleblocks_on_sheet(sheet):
    """
    Returns all Titleblocks on Sheet
    """
    titleblock_category_id = doc.Settings.Categories.get_Item(DB.BuiltInCategory.OST_TitleBlocks).Id

    elements_on_sheet = DB.FilteredElementCollector(doc).OwnedByView(sheet.Id)

    titleblocks = []

    for element in elements_on_sheet:
        if not element.Category:
            continue

        if element.Category.Id == titleblock_category_id:
            titleblocks.append(element)

    return titleblocks

def duplicate_sheet(sheet, number=None, name=None, duplicate_option=DB.ViewDuplicateOption.WithDetailing):
    """
    Duplicates sheet with all Views
    """
    # Get all Viewports and Titleblock from Sheet
    viewport_ids = sheet.GetAllViewports()

    titleblocks = titleblocks_on_sheet(sheet)

    titleblock = titleblocks[0] # Quick workaround

    with DB.Transaction(doc, "Create Sheet") as t:
        t.Start()

        sheet_duplicate = DB.ViewSheet.Create(doc, titleblock.GetTypeId())
        sheet_duplicate.Name = sheet.Name

        t.Commit()

    with DB.Transaction(doc, "Duplicate Views and place on Sheet") as t:

        t.Start()

        for viewport_id in viewport_ids:
            viewport = doc.GetElement(viewport_id)
            view_id = viewport.ViewId
            view = doc.GetElement(view_id)

            view_duplicate_id = view.Duplicate(duplicate_option)

            viewport_duplicate = DB.Viewport.Create(doc, sheet_duplicate.Id, view_duplicate_id, viewport.GetBoxCenter())

            # Synchronize Viewport properties
            viewport_duplicate.Rotation = viewport.Rotation

            # viewport_duplicate.Name = viewport.element.get_Parameter(DB.BuiltInParameter.SHEET_NAME)

            viewport_duplicate.ChangeTypeId(viewport.GetTypeId())

        t.Commit()

    return sheet_duplicate

# Select Sheets
sheets = forms.select_sheets(use_selection=True)

options = {
 	"Duplicate view": DB.ViewDuplicateOption.Duplicate,
 	"Duplicate as Dependent": DB.ViewDuplicateOption.AsDependent,
 	"Duplicate with Detailing" : DB.ViewDuplicateOption.WithDetailing
}

selected_option = forms.CommandSwitchWindow.show(
    options.keys(),
    message='Duplicate option'
)

option = options[selected_option]


if sheets:
    tg = DB.TransactionGroup(doc, __title__)
    tg.Start()

    sheets_new = []

    for sheet in sheets:
        sheet_new = duplicate_sheet(sheet, duplicate_option=option)
        uidoc.ActiveView = sheet_new

    tg.Assimilate()
