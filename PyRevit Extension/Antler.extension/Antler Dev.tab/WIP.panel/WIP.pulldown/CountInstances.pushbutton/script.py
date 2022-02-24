# from System.Collections.Generic import *
from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

import antler.ui
import math

uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()
config = script.get_config()


def configure(config, category):
    # Set instance parameter selection for category.
    parameters = antler.ui.select_instance_parameters_of_category(category)
    logger.debug(parameters)
    #
    # config.configured = True
    # script.save_config()


if not config.has_option('configured') or EXEC_PARAMS.config_mode:
    # Select category
    categories = antler.ui.select_category()
    for category in categories:
        logger.debug(category)
        configure(config, category)



# print(dir(script))

# Get all doors and windows
collector = DB.FilteredElementCollector(doc)

collector.OfCategory(
    DB.BuiltInCategory.OST_Doors).WhereElementIsNotElementType()

elements = collector.ToElements()
