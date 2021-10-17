# -*- coding: utf-8 -*-

# from System.Collections.Generic import *
from rpw import revit, DB, UI

# from pyrevit import forms
from collections import OrderedDict

import time
start_time = time.time()


__doc__ = "Cycle Family Types"
__title__ = "Next Type"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc


def cycle_family_type(element, next=True):
    family = element.Symbol.Family

    symbol_ids = family.GetFamilySymbolIds()
    symbols = [doc.GetElement(id) for id in symbol_ids]
    symbol_names = [s.get_Parameter(
        DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString() for s in symbols]

    symbol_id_dict = {name: id for name, id in zip(symbol_names, symbol_ids)}
    symbol_id_dict = OrderedDict(sorted(symbol_id_dict.items()))

    symbol_dict = {name: symbol for name, symbol in zip(symbol_names, symbols)}
    symbol_dict = OrderedDict(sorted(symbol_dict.items()))


    index = symbol_id_dict.values().index(element.Symbol.Id)

    if next:
        next_index = index + 1
    else:
        next_index = index - 1

    next_index = next_index % len(symbol_ids)

    next_symbol = symbol_dict.values()[next_index]

    element.Symbol = next_symbol

    return element


elements = [doc.GetElement(id) for id in uidoc.Selection.GetElementIds()]


if elements:
    for element in elements:
        with DB.Transaction(doc, __title__) as t:
            t.Start()

            for element in elements:
                cycle_family_type(element, next=True)

            t.Commit()

# print("--- %s seconds ---" % (time.time() - start_time))
