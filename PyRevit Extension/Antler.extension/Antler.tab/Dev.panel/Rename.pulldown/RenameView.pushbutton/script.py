from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

import antler.util
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
    try:
        default = config.input_string
    except:
        default = ''

    input_string = forms.ask_for_string(
        default=default,
        prompt='Enter View name template: {}',
        title='Enter View Template'
    )

    config.input_string = input_string
    script.save_config()

    with DB.Transaction(doc, __commandname__) as t:

        t.Start()

        for view in selected_views:
            try:
                new_name = antler.util.string_from_template(view, input_string)
                logger.info(new_name)

                view.Name = new_name # 'View Name'
            except Exception as e:
                logger.warning("Rename failed: {}".format(e))

        t.Commit()
