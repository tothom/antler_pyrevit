# -*- coding: utf-8 -*-
from rpw import DB, revit
from pyrevit import forms, script

from collections import OrderedDict

import antler

logger = script.get_logger()

docs = antler.forms.select_docs() or script.exit()
logger.debug(docs)
# docs = docs or []

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
    'Walls': DB.BuiltInCategory.OST_Walls,
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

logger.debug(builtin_category)


for doc in docs:
    type_elements = DB.FilteredElementCollector(doc).OfCategory(
        builtin_category).WhereElementIsElementType().ToElements()

    logger.debug(type_elements)

    # report_dict = OrderedDict()

    report = []

    for type_element in type_elements:

        instance_elements = antler.collectors.collect_instances_of_element_type(type_element)
        count = len(instance_elements)#.GetElementCount()

        logger.debug(type_element)

        name = type_element.get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
        logger.debug(name)

        compound_structure = type_element.GetCompoundStructure()
        width = compound_structure.GetWidth()

        report.append(OrderedDict({
            'Name': name,
            'Count': count,
            'Layers': antler.parameters.compound_structure_summary(compound_structure, sep=';'),
            'Width': DB.UnitFormatUtils.Format(
                        revit.doc.GetUnits(),
                        DB.SpecTypeId.Length,
                        width,
                        False)
            })
        )

    # report_dict = OrderedDict(sorted(report_dict.items()))

    # antler.util.print_dict_as_table(report_dict, title=doc.Title)
    antler.util.print_dict_list(report, title=doc.Title, sort_key="Name")
