# -*- coding: utf-8 -*-

"""
Source: https://thebuildingcoder.typepad.com/blog/2015/12/shared-project-parameter-guid-reporter.html
"""

from rpw import revit, DB, UI
from pyrevit import forms, script
# import re

import antler.util

logger = script.get_logger()

report = []

iterator = revit.doc.ParameterBindings.ForwardIterator()
iterator.Reset()

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
    record['Group'] = definition.ParameterGroup

    record['Is Shared Parameter'] = isinstance(parameter, DB.SharedParameterElement)

    if record['Is Shared Parameter']:
        record['GUID'] = parameter.GuidValue

    # logger.info(record)

    report.append(record)

antler.util.print_dict_list(report)
