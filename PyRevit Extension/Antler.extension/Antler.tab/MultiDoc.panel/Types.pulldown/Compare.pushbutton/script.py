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




source = antler.forms.select_docs(
    selection_filter=lambda x: not x.IsFamilyDocument,
    multiselect=False,
    title="Select document to act as SOURCE."
) or script.exit()

destination_docs = antler.forms.select_docs(
    selection_filter=lambda x: not x.IsFamilyDocument and not x.IsLinked and x != source,
    multiselect=True,
    title="Select DESTINATION documents."
) or script.exit()

category = antler.forms.select_category() or script.exit()

category_ids_where_to_get_instances = (
    DB.ElementId(DB.BuiltInCategory.OST_Materials),
)

collector = DB.FilteredElementCollector(source).OfCategoryId(category.Id)

if category.Id in category_ids_where_to_get_instances:
    collector.WhereElementIsNotElementType()
    # print("Hello!")
else:
    collector.WhereElementIsElementType()

elements = collector.ToElements()

match_parameter = revit_types.select_match_parameter(category, source)

# match_parameter = revit_types.select_match_parameter(category, source)
# match_parameter = 'GUID'
# match_parameter = 'Type Name'


for destination_doc in destination_docs:
    diff = revit_types.find_and_compare_elements(
        elements, destination_doc, match_parameter, exceptions=['Type IfcGUID'])

    logger.info(diff)

    # if diff:
    #     selected_option = forms.alert(
    #         'Differences found. Overwrite destination?',
    #         options=["Overwrite", "Cancel"],
    #     ) or script.exit()
    # else:
    #     continue

    if diff:
        with DB.Transaction(destination_doc, __commandname__) as t:
            t.Start()
            for comparison in diff:
                destination_parameter = comparison['Destination'].get_Parameter(
                    comparison['Definition'])

                # source_value = antler.parameters.get_parameter_value(source_parameter)
                source_value = comparison['Value']

                if not destination_parameter:
                    continue

                if destination_parameter.StorageType != DB.StorageType.ElementId and not destination_parameter.IsReadOnly:
                    antler.parameters.set_parameter_value(
                        destination_parameter, source_value)

                elif destination_parameter.Definition.Name in ('Type Name'):
                    existing_value = antler.parameters.get_parameter_value(
                        destination_parameter)

                    if str(source_value) != str(existing_value):
                        try:
                            comparison['Destination'].Name = source_value
                        except Exception as e:
                            logger.warning(e)
                else:
                    logger.debug("Parameter {} is read only".format(
                        destination_parameter.Definition.Name))
            t.Commit()
