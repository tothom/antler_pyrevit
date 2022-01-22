# -*- coding: utf-8 -*-

from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms
from collections import OrderedDict

import os
import csv
import json

__doc__ = "Import types from JSON file and applies changes"
__title__ = "Import Types"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

RESERVED_KEYS = ['Category', 'Family', 'Type', 'Id', 'Count', 'Delete']

def read_csv(file):
	# print('CSV')
	reader = csv.DictReader(file)
	# reader = csv.reader(file)
	data = {'types': []}

	for row in reader:
		data['types'].append(row)

	return data

def read_json(file):
	# print('JSON')
	data = json.load(f)

	return data

read_format_mapper = {
'.csv': read_csv,
'.json': read_json
}

# Read file
file = forms.pick_file()

with open(file, mode='r') as f:
	name, ext = os.path.splitext(file)
	data_dict = read_format_mapper.get(ext)(f)

# print(data_dict)

types = data_dict['types']

with DB.Transaction(doc, __doc__) as t:
	t.Start()

	for item in types:
		element = doc.GetElement(DB.ElementId(int(item['Id'])))
		print(int(item['Id']), element)

		if not element:
			continue

		try:
			if item['Delete'] == True:
				doc.Delete(element.Id)
				continue
		except:
			pass

		for key, value in item.items():
			if not key in RESERVED_KEYS:
				# print(key, value)
				parameter = element.LookupParameter(key)
				# print(parameter.Definition.Name)
				# print(parameter.StorageType)
				if parameter:
					try:
						if parameter.StorageType == DB.StorageType.Integer:
							value = int(value)
						elif parameter.StorageType == DB.StorageType.Double:
							value = float(value)
						# elif parameter.StorageType == DB.StorageType.ElementId:
						# 	value = DB.

						parameter.Set(value)
					except Exception as e:
						print("Exception: {}".format(e))

		element.Name = item['Type']

	t.Commit()
