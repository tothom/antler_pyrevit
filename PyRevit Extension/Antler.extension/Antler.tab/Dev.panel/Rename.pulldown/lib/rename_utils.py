from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

import antler.util

doc = revit.doc

logger = script.get_logger()
config = script.get_config()


def ask_for_template_string():
    try:
        default = config.input_string
    except:
        default = ''

    input_string = forms.ask_for_string(
        default=default,
        prompt='Enter name template: {}',
        title='Enter template'
    )

    config.input_string = input_string
    script.save_config()

    return input_string


def rename_elements(elements, template_string):
    with DB.Transaction(doc, __commandname__) as t:

        t.Start()

        for element in elements:
            try:
                new_name = antler.util.string_from_template(
                    element, template_string)
                logger.info(new_name)

                element.Name = new_name  # 'View Name'
            except Exception as e:
                logger.warning("Rename failed: {}".format(e))

        t.Commit()
