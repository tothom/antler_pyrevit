# -*- coding: utf-8 -*-

from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms
from collections import OrderedDict

from System.Windows import Clipboard

import difflib

import csv
import json

__doc__ = "Quick PDF"
__title__ = "Quick PDF"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc





def get_view_print_name(view):
    # Get file name
    try:
        name = "{} - {}".format(view.SheetNumber, view.Name)
    except:
        name = "{}".format(view.Name)

    return name


view = uidoc.ActiveView

default_name = get_view_print_name(view)

Clipboard.SetText(default_name)

"""
# def print_to_pdf(view, file_path):
# Set file path
file_path = forms.save_file(file_ext='pdf', default_name=default_name)

# Select Views or View Sets
view_set = None
use_current_print_settings = True

# doc.Print(view_set, use_current_print_settings)

# Set print settings
# https://www.revitapidocs.com/2020/81f215a5-8124-ebfc-c637-463f46f80937.htm
print_manager = doc.PrintManager

# print_manager.SelectNewPrintDriver("Microsoft Print to PDF")
print_manager.PrintToFile = True
print_manager.CombinedFile = False
print_manager.PrintToFileName = default_name

settings = print_manager.PrintSetup.InSession

paper_size = GetPaperSize(sheet)

settings.PrintParameters.PageOrientation = paperSize.PageOrientation

print_manager.PrintSetup.CurrentPrintSetting = settings
# print_manager.PrintSetup.SaveAs("Tempsetting" + plotSettingsNumber.ToString())

# print_manager.Apply()
print_result = print_manager.SubmitPrint(sheet)
"""
