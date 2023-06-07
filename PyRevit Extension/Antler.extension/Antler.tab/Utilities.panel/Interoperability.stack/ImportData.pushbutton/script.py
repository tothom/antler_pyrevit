# -*- coding: utf-8 -*-

from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script, EXEC_PARAMS
from collections import OrderedDict, defaultdict

import os
# import csv
import unicodecsv as csv
import re

import antler

logger = script.get_logger()
# schedule = forms.select_view.show()


# def set_parameter_by_name(element, parameter_name, value):
#     parameters = element.GetParameters(parameter_name)
#     logger.debug(parameters)
#     logger.debug([a.Definition.Name for a in parameters])
#
#     # Workaround because 'Sheet Number' returns two parameters...
#     if parameter_name == 'Sheet Number':
#         parameters = parameters[:1]
#
#     # logger.debug(parameters.Count)
#
#     if parameters.Count == 1:
#         parameter = parameters[0]
#
#         if not parameter.IsReadOnly:  # parameter.UserModifiable
#             # convert = PARAMETER_SET_MAPPING.get(parameter.StorageType)
#             # # if convert is not None:
#             # converted_value = convert(value)
#             try:
#                 antler.parameters.set_parameter_value(parameter, value)
#             except Exception as e:
#                 logger.debug("{} {}".format(type(e), e))
#     elif parameters.Count == 0:
#         logger.warning(
#             "No parameters with name {} found".format(parameter_name))
#     elif parameters.Count > 1:
#         logger.warning(
#             "Parameter name {} is ambigous and is skipped".format(parameter_name))


def interpret_schedule_data(data):
    """
    """
    for key, value in item.items():
        if value is None:
            continue

        pattern = '(.*)(\<.*>)'
        match = re.match(pattern, key)

        if not match:
            logger.warning("No parameter with name {} found.".format(key))
            continue

        parameter_name = match.group(1).strip()
        parameter_type = match.group(2).strip()

        logger.debug(parameter_type)
        logger.debug(parameter_name)
        logger.debug(value)

        assert parameter_type and parameter_name

        if parameter_type == '<Instance>':
            result = set_parameter_by_name(element, parameter_name, value)

        elif parameter_type == '<Type>':
            result = set_parameter_by_name(element_type, parameter_name, value)


# def sanitize_dict(dictionary)

def interpret_data(data):
    # interpreted_data = {}
    structured_data = defaultdict(dict)

    for item in data:
        parameter_dict = {}

        # item = {}

        doc_name = item.pop('~Document')

        doc = antler.collectors.get_doc_by_name(
            doc_name, filter_func=lambda x: not x.IsLinked)

        if not doc:
            continue
        else:
            # if not doc in structured_data:
            #     structured_data[doc] = {}


            if '~UniqueId' in item:
                element_unique_id = item.pop('~UniqueId')
                element = doc.GetElement(element_unique_id)
            else:
                element_id = DB.ElementId(int(item.pop('~ElementId')))
                element = doc.GetElement(element_id)
                
            # element_type = revit.doc.GetElement(element.GetTypeId())

            # logger.debug(element)

            if element:
                for key, value in item.items():
                    if key and not key.startswith('~'):
                        parameter = element.LookupParameter(key)

                        logger.debug((value, type(value)))

                        if parameter:
                            parameter_dict[parameter] = value
                        else:
                            logger.info('Parameter with name "{}" not found'.format(
                                key))

            structured_data[doc].update({element: parameter_dict})

    return structured_data


# Open and read CSV
file = forms.pick_file(file_ext='csv') or script.exit()
#
# if not file:
#     script.exit()

if EXEC_PARAMS.config_mode:
    delimiter = forms.CommandSwitchWindow.show(
        [',', ';'],
        message='Select CSV delimiter'
    ) or script.exit()
else:
    delimiter = ';'

# delimiter = delimiter or s

with open(file, mode='r') as f:
    reader = csv.DictReader(f, delimiter=delimiter,
                            encoding='utf-8-sig')  # , quotechar='"',
    # quoting=csv.QUOTE_MINIMAL)
    import_list = []

    i = 0

    for row in reader:
        # if i < 10:
        logger.debug(row)
        import_list.append(row)
        # i += 1

logger.debug(import_list)

data = interpret_data(import_list)

output = script.get_output()

# Apply changes from CSV
for doc, element_dict in data.items():
    output.print_md("## Processing {doc}".format(
        doc=doc.Title
    ))

    # if not doc:
    if doc.IsLinked:
        print("Please open Document {doc_name} to import data.".format(
            doc_name=doc.Title
        ))
        continue
    else:
        with DB.Transaction(doc, __commandname__) as tg:
            tg.Start()

            logger.debug("Transaction started.")

            for element, parameter_dict in element_dict.items():
                for parameter, value in parameter_dict.items():
                    logger.debug((parameter.Definition.Name, value))
                    logger.debug(parameter.StorageType)

                    if value is None or parameter.IsReadOnly or parameter.StorageType != DB.StorageType.ElementId::
                        continue

                    try:
                        if parameter.Definition.Name in ('Type Name',):
                            existing_value = antler.parameters.get_parameter_value(
                                parameter)
                            if not value:
                                continue
                            elif str(value) != str(existing_value):
                                element.Name = value

                        else:
                            existing_value = antler.parameters.get_parameter_value(
                                parameter)

                            if value in (None, '') and existing_value in (None, ''):
                                continue

                            elif str(value) != str(existing_value):
                                antler.parameters.set_parameter_value(
                                    parameter, value)

                    except Exception as e:
                        logger.warning(e)

                    else:
                        output.print_md("{element}: Parameter '{def_name}' changed from '{existing_value}' to **'{value}'**".format(
                            element=output.linkify(element.Id),
                            def_name=parameter.Definition.Name,
                            existing_value=existing_value,
                            value=value,
                            equals='are equal' if str(value) != str(
                                existing_value) else 'are not equal'
                        ))
            tg.Commit()

output.print_md("# Done!")
