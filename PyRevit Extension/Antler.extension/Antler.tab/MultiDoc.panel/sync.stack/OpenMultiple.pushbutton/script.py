# -*- coding: utf-8 -*-
from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

from Autodesk.Revit.Exceptions import InvalidOperationException

from Microsoft.Win32 import OpenFileDialog

logger = script.get_logger()
output = script.get_output()


def rvt_file_dialog():
    dialog = OpenFileDialog()
    # Filter files by extension
    dialog.Filter = "Revit file types (*.rvt, *.rfa, *.rte)|*.rvt;*.rfa;*.rte"
    dialog.Multiselect = True

    result = dialog.ShowDialog()

    return dialog.FileNames


filenames = rvt_file_dialog()

for filename in filenames:
    file_info = DB.BasicfileInfo.Extract(filename)

    if file_info.IsWorkshared:
        if file_info.IsLocal:
            try:
                revit.uiapp.OpenAndActivateDocument(filename)
            except Exception as e:
                logger.warning(e)
        elif file_info.IsCentral:
            logger.warning("Script does not open yet Central Models.")
    else:
        try:
            revit.uiapp.OpenAndActivateDocument(filename)
        except Exception as e:
            logger.warning(e)
