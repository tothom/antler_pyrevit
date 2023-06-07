
# Get script environment
# from System import Environment

# print(Environment.MachineName)


# Get logger
global LOGGER
try:
    from pyrevit import script
    LOGGER = script.get_logger()
except:
    import logging
    LOGGER = logging.getLogger(__name__)


# Global imports
try:
    from rpw import DB
    from rpw import revit

    DOC = revit.doc
except Exception as e:
    LOGGER.warning(e)
    LOGGER.warning("Failed to import Revit Python Wrapper.")


# Package imports
import analysis
import interop
import ui
# import transform
import utils
import color
import compare
import collectors
import filters
import forms
import views
import instances
import parameters
# import analysis


# # reload(util)
