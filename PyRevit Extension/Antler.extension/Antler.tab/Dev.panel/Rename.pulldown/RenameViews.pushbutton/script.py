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
# Preselect Views
selected_element_ids = uidoc.Selection.GetElementIds()

selected_views = []

for element_id in selected_element_ids:
    element = doc.GetElement(element_id)

    if isinstance(element, DB.View):
        selected_views.append(element)

# Select Views
if not selected_views:
    selected_views = forms.select_views(
        title="Select Views to rename"
    )

if selected_views:
    input_string = rename_utils.ask_for_template_string()

    rename_utils.rename_elements_with_template(selected_views, input_string)
