# -*- coding: utf-8 -*-
from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

from Autodesk.Revit.Exceptions import InvalidOperationException

from Microsoft.Win32 import OpenFileDialog

logger = script.get_logger()
output = script.get_output()

def rvt_file_dialog():
    dialog = OpenFileDialog()
    dialog.Filter = "Revit model (.rvt)|*.rvt" # Filter files by extension
    dialog.Multiselect = True

    result = dialog.ShowDialog()

    return dialog.FileNames

filenames = rvt_file_dialog()

if filenames:
    for filename in filenames:
        try:
            revit.uiapp.OpenAndActivateDocument(filename)
        except Exception as e:
            logger.warning(e)
