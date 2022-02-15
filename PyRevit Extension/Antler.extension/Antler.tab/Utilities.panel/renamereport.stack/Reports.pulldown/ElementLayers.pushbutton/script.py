# -*- coding: utf-8 -*-


from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS
import re
from System.Collections.Generic import List
import clr

from collections import OrderedDict

import antler

uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()




docs = antler.forms.select_docs()

logger.debug(docs)

docs = docs or []

# select_compound_classes
compound_classes = [
    DB.Floor,
    DB.RoofBase,
    DB.Wall,
    DB.Ceiling
]

# select_compound_classes
compound_categories_dict = {
    'Floors': DB.BuiltInCategory.OST_Floors,
    # 'RoofBase',
    # 'Wall',
    # 'Ceiling'
}

selected = forms.SelectFromList.show(
    sorted(compound_categories_dict.keys()),
    button_name='Select Categories',
    multiselect=False
)

builtin_category = compound_categories_dict[selected]

# compound_classes_list = List[None](compound_classes)
# element_multiclass_filter = DB.ElementMulticlassFilter(compound_classes_list)
# collector = DB.FilteredElementCollector(revit.doc).WhereElementIsElementType().WherePasses(element_multiclass_filter)
# type_elements = collector.ToElements()
# print(type_elements)

for doc in docs:
    type_elements = DB.FilteredElementCollector(doc).OfCategory(
        builtin_category).WhereElementIsElementType().ToElements()

    # logger.info(type_elements)

    # report_dict = OrderedDict()

    report = []

    for type_element in type_elements:

        instance_elements = antler.collectors.collect_instances_of_element_type(type_element)
        count = len(instance_elements)#.GetElementCount()

        logger.debug(type_element)

        name = type_element.get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
        logger.debug(name)

        report.append(OrderedDict({
            'Name': name,
            'Count': count,
            'Layers': element_layer_report(type_element, sep=';'),
            })
        )

    # report_dict = OrderedDict(sorted(report_dict.items()))

    # antler.util.print_dict_as_table(report_dict, title=doc.Title)
    antler.util.print_dict_list(report, title=doc.Title, sort_key="Name")
