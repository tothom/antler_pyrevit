# -*- coding: utf-8 -*-

from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms
from collections import OrderedDict

import csv
import json

__doc__ = "Exports drawing as image and imports it back as overlay. Overlay image can be overriden to synchronize sketch with Revit"
__title__ ="Quick Image Overlay"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

def get_view_centre_point(view):
    """
    Returns view center point in model units. Works only for plan views and sheets.
    """
    centre_pt = DB.XYZ(
        (view.Outline.Max.U + view.Outline.Min.U) / 2.0 * view.Scale,
        (view.Outline.Max.V + view.Outline.Min.V) / 2.0 * view.Scale,
        0
    )

    return centre_pt

# Get file name
try:
    default_name = "{} - {}".format(uidoc.ActiveView.SheetNumber, uidoc.ActiveView.Name)
except:
    default_name = "{}".format(uidoc.ActiveView.Name)

# EXPORT IMAGE FROM VIEW
file_path = forms.save_file(file_ext='png', default_name=default_name)

if file_path:
    # Select DPI
    dpi_options = {
        72: DB.ImageResolution.DPI_72,
        150: DB.ImageResolution.DPI_150,
        300: DB.ImageResolution.DPI_300,
        600: DB.ImageResolution.DPI_600,
        }

    dpi_options = OrderedDict(sorted(dpi_options.items(), key=lambda t: t[0]))

    selected_dpi = forms.CommandSwitchWindow.show(
        dpi_options.keys(),
        message='Image DPI'
        )

    # EXPORT IMAGE FROM VIEW
    image_export_options = DB.ImageExportOptions()

    image_export_options.FilePath = file_path

    image_export_options.ZoomType = DB.ZoomFitType.Zoom
    image_export_options.Zoom = 100
    # image_export_options.FitDirection = DB.FitDirectionType.Horizontal
    # image_export_options.PixelSize = 1024

    image_export_options.HLRandWFViewsFileType = DB.ImageFileType.PNG
    image_export_options.ShadowViewsFileType = DB.ImageFileType.PNG
    image_export_options.ImageResolution = dpi_options[selected_dpi]
    image_export_options.ExportRange = DB.ExportRange.CurrentView

    doc.ExportImage(image_export_options)

    # IMPORT PREVIOUSLY EXPORTED IMAGE
    # https://www.revitapidocs.com/2019/b45a2657-8cdf-6471-4929-a758d1675b17.htm
    # Revit 2020 > only...
    # """

    with DB.Transaction(doc, __title__) as t:
        t.Start()

        image_type_options = DB.ImageTypeOptions(file_path)
        # image_type_options.Resolution = selected_dpi
        image_type = DB.ImageType.Create(doc, image_type_options)

        # print(uidoc.ActiveView.BoundingBox)
        # location = get_view_centre_point(uidoc.ActiveView)

        # if isinstance(uidoc.ActiveView, DB.ViewSheet):
        #     location = uidoc.ActiveView.Origin
        # else:

        centre_pt = get_view_centre_point(uidoc.ActiveView)

        # location = uidoc.ActiveView.Origin
        location = centre_pt

        # print(location)

        image_placement_options = DB.ImagePlacementOptions(location, DB.BoxPlacement.Center)
        image = DB.ImageInstance.Create(doc, uidoc.ActiveView, image_type.Id, image_placement_options)

        image_scale = uidoc.ActiveView.Scale / float(selected_dpi) * 72.0
        image.WidthScale = image_scale
        image.DrawLayer = DB.DrawLayer.Foreground

        t.Commit()
