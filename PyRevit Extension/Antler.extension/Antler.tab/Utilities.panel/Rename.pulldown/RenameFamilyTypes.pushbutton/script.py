from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

import antler.util
import rename_utils
reload(antler.util)

doc = revit.doc
uidoc = revit.uidoc

logger = script.get_logger()
config = script.get_config()

# Select
families = antler.ui.select_families()

# script.exit()

if families:
    input_string = rename_utils.ask_for_template_string()

    family_symbols = []

    for family in families:
        family_symbols.extend([doc.GetElement(id) for id in family.GetFamilySymbolIds()])

    rename_utils.rename_elements(family_symbols, input_string)
