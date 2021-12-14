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

if filenames:
    print("Trying to open {0} files...".format(len(filenames)))
    output.indeterminate_progress(True)

for i, filename in enumerate(filenames):
    print("Trying to open {0}...".format(filename))

    try:
        revit.uiapp.OpenAndActivateDocument(filename)
    except Exception as e:
        logger.warning(e)
    else:
        print("{0} succesfully opened...".format(filename))

    output.indeterminate_progress(False)
    output.update_progress(i + 1, len(filenames))
