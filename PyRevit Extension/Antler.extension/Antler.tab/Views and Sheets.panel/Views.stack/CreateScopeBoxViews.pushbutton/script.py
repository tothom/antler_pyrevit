from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms
from collections import OrderedDict

__doc__ = "Creates Dependent Views from existing Views and Scope Boxes."
__title__ = "Create\nScope Box Views"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc


# Select Views
views = forms.select_views()

# Select Scope Boxes
scope_boxes = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_VolumeOfInterest).WhereElementIsNotElementType().ToElements()

scope_box_dict = {"{}".format(a.Name): a for a in scope_boxes}

# levels_dict = OrderedDict(sorted(levels_dict.items(), key=lambda (key, value): value.Elevation, reverse=True))
scope_box_keys = forms.SelectFromList.show(scope_box_dict.keys(), multiselect=True, title='Select Scope Boxes')

if scope_box_keys:
    scope_boxes_selected = [scope_box_dict.get(key) for key in scope_box_keys] # Using get() to avoid error message when cancelling dialog.
else:
    scope_boxes_selected = []

# print(views, scope_boxes_selected)

if views and scope_boxes_selected:
    with DB.Transaction(doc, __title__) as t:
        t.Start()

        for view in views:

            for scope_box in scope_boxes_selected:
                view_new_id = view.Duplicate(DB.ViewDuplicateOption.AsDependent)
                view_new_elem = doc.GetElement(view_new_id)

                param = view_new_elem.get_Parameter(DB.BuiltInParameter.VIEWER_VOLUME_OF_INTEREST_CROP) # Gets Scope Box of View
                param.Set(scope_box.Id)

                view_new_elem.Name = "{} - {}".format(view_new_elem.Name, scope_box.Name)

        t.Commit()
