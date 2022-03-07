# from System.Collections.Generic import *
from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

import antler.geometry.transform
import math

import doors_and_windows_utils

uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()
config = script.get_config()


def configure(config):
    # Set handing parameter
    door = DB.FilteredElementCollector(doc).OfCategory(
        DB.BuiltInCategory.OST_Doors).WhereElementIsNotElementType().FirstElement()
    window = DB.FilteredElementCollector(doc).OfCategory(
        DB.BuiltInCategory.OST_Windows).WhereElementIsNotElementType().FirstElement()

    door_parameter_names = []

    for parameter in door.ParametersMap:
        if parameter.StorageType == DB.StorageType.String:
            door_parameter_names.append(parameter.Definition.Name)

    window_parameter_names = []

    for parameter in window.ParametersMap:
        if parameter.StorageType == DB.StorageType.String:
            window_parameter_names.append(parameter.Definition.Name)

    parameter_names = set(door_parameter_names).intersection(
        set(window_parameter_names))

    config.parameter_name = forms.SelectFromList.show(
        sorted(parameter_names),
        button_name='Select Parameter',
        multiple=False,
        message='Select parameter to write door and window handing to.')

    if not config.parameter_name:
        script.exit()

    config.right_string = forms.ask_for_string(
        prompt="Enter right text",
        title="Right text"
    )

    config.left_string = forms.ask_for_string(
        prompt="Enter left text",
        title="Left text"
    )

    config.configured = True
    script.save_config()


if not config.has_option('configured') or EXEC_PARAMS.config_mode:
    configure(config)


# print(dir(script))

# Get all doors and windows
collector = DB.FilteredElementCollector(doc)
collector.OfCategory(
    DB.BuiltInCategory.OST_Doors).WhereElementIsNotElementType()
doors = collector.ToElements()

collector = DB.FilteredElementCollector(doc)
collector.OfCategory(
    DB.BuiltInCategory.OST_Windows).WhereElementIsNotElementType()
windows = collector.ToElements()

elements = list(doors) + list(windows)

with DB.Transaction(doc, __commandname__) as t:
    t.Start()

    for element in elements:
        parameter = element.LookupParameter(config.parameter_name)
        doors_and_windows_utils.write_handing(
            element, parameter, right_string=config.right_string, left_string=config.left_string)

    t.Commit()
