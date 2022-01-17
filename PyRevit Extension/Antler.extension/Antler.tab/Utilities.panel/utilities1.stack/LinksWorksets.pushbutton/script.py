# -*- coding: utf-8 -*-

from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms
from collections import OrderedDict

import os
import csv
import json

import antler

workset_table = revit.doc.GetWorksetTable()

revit_link_instances = antler.collectors.revit_link_instances_collector().ToElements()

selected_instances = antler.forms.select_elements(revit_link_instances,
	naming_function=lambda x:"{name} ({workset})".format(
		name=x.Name, workset=workset_table.GetWorkset(x.WorksetId).Name
		)
	)

# print(selected_instances)

workset = antler.forms.select_worksets(multiselect=False)

if workset:
	with DB.Transaction(revit.doc, __commandname__) as tg:
		tg.Start()

		for instance in selected_instances:
			parameter = instance.get_Parameter(DB.BuiltInParameter.ELEM_PARTITION_PARAM)

			parameter.Set(workset.Id.IntegerValue)

		tg.Commit()
