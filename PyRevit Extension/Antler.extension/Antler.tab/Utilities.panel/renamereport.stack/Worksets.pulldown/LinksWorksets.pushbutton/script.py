# -*- coding: utf-8 -*-

from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script
import clr

import antler

logger = script.get_logger()

workset_table = revit.doc.GetWorksetTable()

revit_link_instances = antler.collectors.revit_link_instances_collector().ToElements()

selected_link_instances = antler.forms.select_elements(revit_link_instances,
	naming_function=lambda x:"{name} ({workset})".format(
		name=x.Name, workset=workset_table.GetWorkset(x.WorksetId).Name
		)
	)

# revit_link_types = antler.collectors.revit_link_types_collector().ToElements()
#
# revit_link_types_dict = {}
#
# for item in revit_link_types:
# 	logger.info(item)
# 	# logger.info(dir(item))
# 	try:
# 		# resource = item.GetExternalResourceReference()
# 		efr = item.GetExternalFileReference()
# 		path = efr.GetPath()
#
# 		key = path.CentralServerPath
#
# 		revit_link_types_dict[key] = item
# 	except Exception as e:
# 		logger.warning(e)
#
# keys = forms.SelectFromList.show(
# 	sorted(revit_link_types_dict.keys()),
# 	title='Select Links',
# 	multiselect=True
# )
#
# selected = [revit_link_types_dict[key] for key in keys]

# selected = antler.forms.select_elements(
# 	revit_link_types_dict.items(),
# 	naming_function=lambda x:x
# 	)


workset = antler.forms.select_worksets(multiselect=False)

if workset:
	with DB.Transaction(revit.doc, __commandname__) as tg:
		tg.Start()

		for link_instance in selected_link_instances:
			link_type = clr.Convert(revit.doc.GetElement(link_instance.GetTypeId()), DB.RevitLinkType)

			instance_parameter = link_instance.get_Parameter(DB.BuiltInParameter.ELEM_PARTITION_PARAM)
			link_parameter = link_type.get_Parameter(DB.BuiltInParameter.ELEM_PARTITION_PARAM)

			logger.debug(link_instance)
			logger.debug(link_type)
			logger.debug(instance_parameter)
			logger.debug(link_parameter)

			try:
				instance_parameter.Set(workset.Id.IntegerValue)
			except Exception as e:
				logger.warning(link_instance.Name)
				logger.warning(e)

			try:
				link_parameter.Set(workset.Id.IntegerValue)
			except Exception as e:
				logger.warning(link_instance.Name)
				logger.warning(e)



		tg.Commit()
