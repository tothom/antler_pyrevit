# -*- coding: utf-8 -*-

from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms
from collections import OrderedDict

import random

import time
start_time = time.time()



__doc__ = "Assign Random Family Types"
__title__ = "Random Type"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc


def random_type(element, next=True):
    family = element.Symbol.Family

    symbol_ids = list(family.GetFamilySymbolIds())

    symbol_id = random.choice(symbol_ids)


    element.Symbol = doc.GetElement(symbol_id)

    return element


elements = [doc.GetElement(id) for id in uidoc.Selection.GetElementIds()]


if elements:
    for element in elements:
        with DB.Transaction(doc, __title__) as t:
            t.Start()

            for element in elements:
                random_type(element, next=True)

            t.Commit()

# print("--- %s seconds ---" % (time.time() - start_time))
