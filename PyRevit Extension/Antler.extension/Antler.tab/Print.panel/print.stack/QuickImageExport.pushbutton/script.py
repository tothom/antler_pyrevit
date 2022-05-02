# -*- coding: utf-8 -*-

from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, EXEC_PARAMS, script
from collections import OrderedDict

import csv
import json

uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()


def get_view_pixel_resolution(view, dpi):
    bbox = view.Outline

    u_dim = bbox.Max.U - bbox.Min.U
    v_dim = bbox.Max.V - bbox.Min.V

    return (int(u_dim * 12 * dpi), int(v_dim * 12 * dpi))


# Get file name
try:
    default_name = "{project_name} - {sheet_number} - {view_name}".format(
        project_name=doc.ProjectInformation.Name,
        sheet_number=uidoc.ActiveView.SheetNumber,
        view_name=uidoc.ActiveView.Name)
except:
    default_name = "{project_name} - {view_name}".format(
        project_name=doc.ProjectInformation.Name,
        view_name=uidoc.ActiveView.Name)


resolutions = (
    (72, DB.ImageResolution.DPI_72),
    (150, DB.ImageResolution.DPI_150),
    (300, DB.ImageResolution.DPI_300),
    (600, DB.ImageResolution.DPI_600),
)

# [logger.info(get_view_pixel_resolution(revit.uidoc.ActiveView, dpi)) for dpi in dpi_options.keys()]
dpi_options = OrderedDict()

for dpi, image_resolution in resolutions:
    pixel_resolution = get_view_pixel_resolution(revit.uidoc.ActiveView, dpi)

    dpi_options["{} {}".format(dpi, pixel_resolution)] = image_resolution

selected_option = forms.CommandSwitchWindow.show(
    dpi_options.keys(),
    message='Image DPI'
) or script.exit()

file_path = forms.save_file(
    file_ext='png', default_name=default_name) or script.exit()

image_export_options = DB.ImageExportOptions()

image_export_options.FilePath = file_path

image_export_options.ZoomType = DB.ZoomFitType.Zoom
image_export_options.Zoom = 100

# image_export_options.FitDirection = DB.FitDirectionType.Horizontal
# image_export_options.PixelSize = 1024

image_export_options.HLRandWFViewsFileType = DB.ImageFileType.PNG
image_export_options.ShadowViewsFileType = DB.ImageFileType.PNG
image_export_options.ImageResolution = dpi_options[selected_option]

if EXEC_PARAMS.config_mode:
    image_export_options.ExportRange = DB.ExportRange.VisibleRegionOfCurrentView
else:
    image_export_options.ExportRange = DB.ExportRange.CurrentView

doc.ExportImage(image_export_options)
