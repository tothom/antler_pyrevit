from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

import antler.util
import rename_utils
# reload(antler.util)

doc = revit.doc
uidoc = revit.uidoc

logger = script.get_logger()
config = script.get_config()

# Select Views
selected_views_or_sheets = antler.ui.preselect((DB.View, DB.ViewSheet))

# If Sheet is selected, get the views on the sheet.
if selected_views_or_sheets:
    selected_views = []
    for element in selected_views_or_sheets:
        if isinstance(element, DB.ViewSheet):
            view_ids = element.GetAllPlacedViews()
            selected_views.extend([doc.GetElement(id) for id in view_ids])

        # else:
        #     if element.ViewType == ViewType.Legend:
        #         pass
        #     else:
        selected_views.append(element)

# Select Views by menu if not views were already selected.
else:
    selected_views = forms.select_views(
        title="Select Views to rename"
    )

if selected_views:
    input_string = rename_utils.ask_for_template_string()
    rename_utils.rename_elements(selected_views, input_string)
