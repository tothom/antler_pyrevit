# -*- coding: utf-8 -*-

from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms
from collections import OrderedDict

import csv
import json

__doc__ = "Quick PNG image export."
__title__ = "Quick Image"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

# Get file name
try:
    default_name = "{} - {}".format(uidoc.ActiveView.SheetNumber,
                                    uidoc.ActiveView.Name)
except:
    default_name = "{}".format(uidoc.ActiveView.Name)

# EXPORT IMAGE FROM VIEW
file_path = forms.save_file(file_ext='png', default_name=default_name)


if file_path:
    dpi_options = {
        72: DB.ImageResolution.DPI_72,
        150: DB.ImageResolution.DPI_150,
        300: DB.ImageResolution.DPI_300,
        600: DB.ImageResolution.DPI_600,
    }

    dpi_options = OrderedDict(sorted(dpi_options.items(), key=lambda t: t[0]))

    selected_option = forms.CommandSwitchWindow.show(
        dpi_options.keys(),
        message='Image DPI'
    )

    image_export_options = DB.ImageExportOptions()

    image_export_options.FilePath = file_path

    image_export_options.ZoomType = DB.ZoomFitType.Zoom
    image_export_options.Zoom = 100

    # image_export_options.FitDirection = DB.FitDirectionType.Horizontal
    # image_export_options.PixelSize = 1024

    image_export_options.HLRandWFViewsFileType = DB.ImageFileType.PNG
    image_export_options.ShadowViewsFileType = DB.ImageFileType.PNG
    image_export_options.ImageResolution = dpi_options[selected_option]
    image_export_options.ExportRange = DB.ExportRange.CurrentView

    doc.ExportImage(image_export_options)
