from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

import antler.util
import rename_utils
# reload(antler.util)

doc = revit.doc
uidoc = revit.uidoc

logger = script.get_logger()
config = script.get_config()

# Select
selected_sheets = antler.ui.preselect(DB.ViewSheet)

if not selected_sheets:
    selected_sheets = forms.select_sheets(
        title="Select Sheets to rename"
    )

if selected_sheets:
    input_string = rename_utils.ask_for_template_string()
    rename_utils.rename_elements(selected_sheets, input_string)
