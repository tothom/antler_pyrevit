# from System.Collections.Generic import List
from rpw import revit, DB, UI

from pyrevit import forms, script, EXEC_PARAMS

# import math
# import clr
import antler
import revit_types

uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()
config = script.get_config()



source = revit.doc

other_docs = antler.forms.select_docs(
    selection_filter=lambda x: not x.IsFamilyDocument,
    multiselect=True,
    title="Select documents where to count elements."
) or script.exit()

category = antler.forms.select_category() or script.exit()

collector = DB.FilteredElementCollector(source).OfCategoryId(category.Id)
collector.WhereElementIsElementType()
elements = collector.ToElements()

common_definitions = antler.parameters.get_definitions_from_elements(
    elements, intersect_set=False)#, hashable_provider=lambda x:x.Definition)

for a in common_definitions:
    logger.debug(a.Name)
    logger.debug(a.ParameterType)

common_definitions = [a for a in common_definitions if a.ParameterType == DB.ParameterType.Integer]
# common_parameters = {k: v for k, v in common_parameters.items(
# ) if v.StorageType == DB.StorageType.Integer}

count_definition = antler.forms.select_elements(
    common_definitions,
    naming_function=lambda x:x.Name,
    title='Select Parameter for element count.',
    multiselect=False
) or script.exit()

# count_definition = common_parameters[parameter_key]

match_parameter = revit_types.select_match_parameter(category, source)


count_dict = {a: 0 for a in elements}

for other_doc in other_docs:
    for element in elements:
        # element_name = antler.parameters.get_element_name(element)

        other_element = antler.compare.find_similar_element(
            element, other_doc, parameter=match_parameter)

        if other_element:
            instances = antler.collectors.get_instances_of_element_type(other_element)
            count_dict[element] += len(instances)

    # diff = find_and_compare_elements(elements, other_doc, match_parameter)


    # if selected_option == 'Overwrite':
with DB.Transaction(source, __commandname__) as t:
    t.Start()
    for element, count in count_dict.items():
        parameter = element.get_Parameter(count_definition)
        try:
            antler.parameters.set_parameter_value(parameter, count)
        except Exception as e:
            logger.warning(e)
    t.Commit()
