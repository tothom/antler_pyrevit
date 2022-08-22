# -*- coding: utf-8 -*-

# from System.Collections.Generic import *
from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

import antler
import antler_revit

logger = script.get_logger()
output = script.get_output()


def get_instance_parameter(titleblock, hint):
    for parameter in titleblock.ParametersMap:
        if parameter.Definition.ParameterType == DB.ParameterType.FamilyType \
        and hint in parameter.Definition.Name:
            return parameter


def set_family_instance_type_parameter_value(sheet, type_hint, family_hint, doc_hint):
    titleblock = antler.collectors.titleblocks_on_sheet_collector(sheet).FirstElement()
    family = titleblock.Symbol.Family

    logger.debug(sheet)

    with DB.Transaction(revit.doc, "Set parameter visibility") as t:
        t.Start()

        parameter = get_instance_parameter(titleblock, family_hint)

        logger.info("Parameter: " + parameter.Definition.Name)

        possible_values = family.GetFamilyTypeParameterValues(parameter.Id)

        value = None

        for i, possible_value in enumerate(possible_values):
            element = revit.doc.GetElement(possible_value)
            # logger.info(element)

            element_name = DB.Element.Name.__get__(element)

            if family_hint.lower() in element.FamilyName.lower() \
                and type_hint in element_name \
                and doc_hint.lower() in element.FamilyName.lower():

                logger.info("Value: {} {}".format(element.FamilyName, element_name))
                value = possible_value
                continue

        logger.debug(value)

        if not value:
            raise ValueError("No possible parameter value found")
        else:
            pass
            parameter.Set(value)


        t.Commit()

HINTS = ['Sør', 'Plan']

doc_hint_dict = {
    '102.07_ARK_Kv A': 'Kv A',
    '102.07_ARK_Kv B': 'Kv B',
}


sheets = forms.select_sheets(use_selection=True) or script.exit()

# Place your code below this line
with DB.TransactionGroup(revit.doc, __commandname__) as tg:
    tg.Start()

    for i, sheet in enumerate(sheets):
        #titleblock = antler.collectors.titleblocks_on_sheet_collector(sheet).FirstElement()
        print("Processing {sheet}".format(
            sheet=sheet.Name
        ))

        for hint in HINTS:
            set_family_instance_type_parameter_value(
                sheet, type_hint=sheet.SheetNumber, family_hint=hint, doc_hint=doc_hint_dict[revit.doc.Title])

        output.update_progress(i+1, len(sheets))

    # tg.Assimilate()
    tg.Commit()
