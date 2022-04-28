# -*- coding: utf-8 -*-

"""
Source: https://thebuildingcoder.typepad.com/blog/2015/12/shared-project-parameter-guid-reporter.html
"""

from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS
import clr
# import re

clr.AddReference("System.Core")
import System
clr.ImportExtensions(System.Linq)

import antler.util

logger = script.get_logger()
output = script.get_output()

def report_parameter_use(doc=revit.doc):
    output = script.get_output()
    output.unhide_progress()
    print("Checking project parameter use...")
    # output.indeterminate_progress(True)

    instance_collector = DB.FilteredElementCollector(revit.doc).WhereElementIsNotElementType()
    instance_count = instance_collector.GetElementCount()

    type_collector = DB.FilteredElementCollector(revit.doc).WhereElementIsElementType()
    type_count = type_collector.GetElementCount()

    total_count = instance_count + type_count
    # print(total_count)

    report = {}

    i = 0

    output.update_progress(i, total_count)

    instance_iterator = instance_collector.GetElementIterator()
    instance_iterator.Reset()

    while instance_iterator.MoveNext():
        element = instance_iterator.Current

        for parameter in element.Parameters:
            key = parameter.Id.IntegerValue

            if not key in report:
                report[key] = 0

            if parameter.HasValue:
                report[key] += 1

        i += 1
        output.update_progress(i + 1, total_count)

    type_iterator = type_collector.GetElementIterator()
    type_iterator.Reset()

    # report = {}

    while type_iterator.MoveNext():
        element = type_iterator.Current

        for parameter in element.Parameters:
            key = parameter.Id.IntegerValue

            if not key in report:
                report[key] = 0

            if parameter.HasValue:
                report[key] += 1

        i += 1
        output.update_progress(i + 1, total_count)

    return report

if EXEC_PARAMS.config_mode:
    parameter_report = report_parameter_use()
else:
    parameter_report = {}

# for key, value in parameter_report.items():
#     print(key, value)

# [print((a.Name, b)) for a, b in parameter_report]

# script.exit()

iterator = revit.doc.ParameterBindings.ForwardIterator()
iterator.Reset()

report = []

while iterator.MoveNext():
    definition = iterator.Key
    binding = iterator.Current
    parameter = revit.doc.GetElement(definition.Id)

    record = {}

    record['Binding Type'] = 'Instance' if isinstance(binding, DB.InstanceBinding) else 'Type'

    try:
        categories = [category.Name for category in binding.Categories]
    except Exception as e:
        logger.debug(e)

    record['Categories'] = categories

    record['Name'] = definition.Name
    record['Parameter Type'] = definition.ParameterType
    record['Group'] = DB.LabelUtils.GetLabelFor(definition.ParameterGroup)

    record['Is Shared Parameter'] = isinstance(parameter, DB.SharedParameterElement)

    if record['Is Shared Parameter']:
        record['GUID'] = parameter.GuidValue

    record['Count'] = parameter_report.get(parameter.Id.IntegerValue, '-')

    # logger.info(record)

    report.append(record)

antler.util.print_dict_list(report, sort_key='Name')
