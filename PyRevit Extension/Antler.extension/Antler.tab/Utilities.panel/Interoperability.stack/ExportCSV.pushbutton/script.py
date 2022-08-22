# -*- coding: utf-8 -*-

# from System.Collections.Generic import List
from rpw import revit, DB

from pyrevit import forms, script, EXEC_PARAMS
# from collections import OrderedDict

import clr
import os
# import json

import antler

#
# class StringOption(forms.TemplateListItem):
#     @property
#     def name(self):
#         return "Option: {}".format(self.item)
#
#
# ops = [MyOption('op1'), MyOption('op2', checked=True), MyOption('op3')]
# res = forms.SelectFromList.show(ops,
#                                 multiselect=True,
#                                 button_name='Select Item')

"""
def build_elements_dict(elements, parameters):
    export_list = []

    for element in elements:
        element_dict = {}

        element_dict['~ElementId'] = element.Id.ToString()

        for parameter in element.Parameters:
            # logger.debug(parameter.Definition.Name)
            # logger.debug(parameter.Id)
            if parameter.Id in parameter_ids:
                logger.debug(parameter.Id)
                # logger.debug(parameter.AsValueString())
                element_dict[parameter.Definition.Name + ' ~Instance'] = parameter.AsString() or parameter.AsValueString()
                #logger.debug(parameter.Id in parameter_ids)

        element_type = revit.doc.GetElement(element.GetTypeId())

        logger.debug(element_type)

        if element_type:
            for parameter in element_type.Parameters:
                if parameter.Id in parameter_ids:
                    logger.debug(parameter.Id)
                    # logger.debug(parameter.AsValueString())
                    element_dict[parameter.Definition.Name + ' ~Type'] = parameter.AsString() or parameter.AsValueString()

        # for parameter_id in field_parameter_ids:
        #     logger.debug(parameter_id)
        #     # parameter = element.get_Parameter(parameter_id)
        #     parameter = revit.doc.GetElement(parameter_id)
        #     logger.debug(parameter)
            # element_dict[parameter.Definition.Name] = parameter.AsValueString()

        export_list.append(element_dict)

    return export_list

def export_elements_in_schedule(schedule_view, xport_types=False, include_links=False, **kwargs):
    schedule_view = revit.uidoc.ActiveView

    links = DB.FilteredElementCollector(schedule_view.Document, schedule_view.Id).OfCategory(DB.BuiltInCategory.OST_RvtLinks).WhereElementIsNotElementType().ToElements()

    for link in links:
        logger.debug(link)
        doc = link.GetLinkDocument()
        logger.debug(doc)

    collector = DB.FilteredElementCollector(
        revit.doc, schedule_view.Id)

    if export_types:
        collector.WhereElementIsElementType()
    else:
        collector.WhereElementIsNotElementType()

    elements = collector.ToElements()

    # if isinstance(schedule_view, DB.ViewSchedule):
    collector = DB.FilteredElementCollector(revit.doc).OfCategoryId(view.Definition.CategoryId)

    collector.WherePasses(view.Definition.GetFilters()[0])

    parameter_ids = []

    for field_index in range(schedule_definition.GetFieldCount()):
        schedule_field = schedule_definition.GetField(field_index)

        parameter_id = schedule_field.ParameterId  # .ToString()

        if parameter_id:
            parameter_ids.append(parameter_id)

    return build_elements_dict(elements, parameter_ids)
    # else:
    #     parameters = None
    #     print("Current View must be a Schedule View")
    #     script.exit()
    #
"""

def select_parameters(elements, title='Select Parameters to Export'):
    parameters = antler.parameters.get_all_parameters(
        elements,
        hashable_provider=antler.parameters.parameter_name_string_provider,
        parameters_provider=lambda x:x.Parameters
        )

    selection = forms.SelectFromList.show(
        sorted(parameters),
        title=title,
        multiselect=True
    )

    return selection


def get_element_parameter_values(elements, parameters):
    elements_dict = {}

    for element in elements:
        category = element.Category
        builtin_category = antler.util.builtin_category_from_category(category)

        element_dict = {
            '~Document': element.Document.Title,
            '~ElementId': element.Id,
            '~UniqueId': element.UniqueId,
            '~Category': DB.LabelUtils.GetLabelFor(builtin_category)
        }

        for parameter_name in parameters:
            parameter = element.LookupParameter(parameter_name)

            if parameter:
                parameter_value = antler.parameters.get_parameter_value(
                    parameter,
                    mapping_overrides={DB.StorageType.ElementId: DB.Parameter.AsValueString})
                # parameter_value = parameter.AsValueString()

                element_dict[parameter_name] = parameter_value

        elements_dict[element] = element_dict

    return elements_dict





def export_materials(docs=[revit.doc], parameter_names=[], get_extended_data=False, **kwargs):
    data = {}

    data['Header'] = "Materials from {docs}".format(
        docs=', '.join([doc.Title for doc in docs])
        )

    materials = []

    material_use_count = {}

    for doc in docs:
        material_collector = antler.collectors.collect_materials(doc)

        materials.extend(material_collector.ToElements())

        if get_extended_data:
            collector = DB.FilteredElementCollector(doc).WhereElementIsElementType()

            element_types = collector.ToElements()

            for element_type in element_types:
                material_ids = element_type.GetMaterialIds(False)

                for material_id in material_ids:
                    if material_id not in material_use_count:
                        material_use_count[material_id] = 1
                    else:
                        material_use_count[material_id] += 1


    parameter_names = parameter_names or select_parameters(materials)

    material_data = get_element_parameter_values(materials, parameter_names)

    if get_extended_data:
        for material in material_data:
            if material.Id in material_use_count:
                material_data[material]['~Count'] = material_use_count[material.Id]
            else:
                material_data[material]['~Count'] = 0
        # for material_id, count in material_use_count.items():
        #     material =

    data['Elements'] = material_data

    return data


def export_elements_of_categories(
        categories=[],
        export_types=False,
        include_links=False,
        count_elements=False,
        get_extended_data=False,
        docs=[revit.doc],
        **kwargs):

    categories = categories or antler.forms.select_category(multiselect=True) or script.exit()

    # builtin_category = clr.Convert(category, DB.BuiltInCategory)
    builtin_categories= [antler.util.builtin_category_from_category(category) for category in categories]
    #
    # logger.debug(builtin_category)

    data = {}

    data['Header'] = "{type_or_instance} elements from {docs}".format(
        type_or_instance='Type' if export_types else "Instance",
        categories=[DB.LabelUtils.GetLabelFor(builtin_category) for builtin_category in builtin_categories],
        docs=', '.join([doc.Title for doc in docs])
        )

    # data['File Name'] = ""{type_or_instance} elements of category [{category}]".format(
    #     type_or_instance='Type' if export_types else "Instance",
    #     category=DB.LabelUtils.GetLabelFor(category)
    #     )

    elements = []

    for doc in docs:
        for category in categories:
            collector = DB.FilteredElementCollector(
                doc).OfCategoryId(category.Id)

            if export_types:
                collector.WhereElementIsElementType()
            else:
                collector.WhereElementIsNotElementType()

            elements.extend(collector.ToElements())

    parameter_names = select_parameters(elements) or script.exit()

    data['Parameters'] = parameter_names

    # logger.debug(elements_dict)

    element_data = get_element_parameter_values(elements, parameter_names)

    if get_extended_data:
        # if builtin_category in (
        #         DB.BuiltInCategory.OST_Floors,
        #         DB.BuiltInCategory.OST_Walls,
        #         DB.BuiltInCategory.OST_Roofs,
        #         DB.BuiltInCategory.OST_Ceilings,
        #         ):
        #
        #     for element in elements:
        #         compound_structure = element.GetCompoundStructure()
        #         if compound_structure:
        #             element_data[element].update({
        #                 '~Layers': antler.parameters.compound_structure_summary(
        #                     compound_structure, sep='\r\n'),
        #             })
        #             element_data[element].update({
        #                 '~LayersShort': antler.parameters.compound_structure_summary(
        #                     compound_structure, sep='-', layer_string_function=antler.parameters.minimal_layer_string),
        #             })
        if export_types:
            for element in elements:
                instance_elements = antler.collectors.get_instances_of_element_type(element)
                count = len(instance_elements)#.GetElementCount()

                element_data[element].update({
                    '~Count': count
                })

    data['Elements'] = element_data

    return data

def export_elements_of_category(
        category=None,
        export_types=False,
        include_links=False,
        count_elements=False,
        get_extended_data=False,
        docs=[revit.doc],
        **kwargs):

    category = category or antler.forms.select_category(multiselect=False) or script.exit()

    # builtin_category = clr.Convert(category, DB.BuiltInCategory)
    builtin_category = antler.util.builtin_category_from_category(category)
    #
    # logger.debug(builtin_category)

    data = {}

    data['Header'] = "{type_or_instance} elements of category [{category}] from {docs}".format(
        type_or_instance='Type' if export_types else "Instance",
        category=DB.LabelUtils.GetLabelFor(builtin_category),
        docs=', '.join([doc.Title for doc in docs])
        )

    # data['File Name'] = ""{type_or_instance} elements of category [{category}]".format(
    #     type_or_instance='Type' if export_types else "Instance",
    #     category=DB.LabelUtils.GetLabelFor(category)
    #     )

    elements = []

    for doc in docs:
        collector = DB.FilteredElementCollector(
            doc).OfCategoryId(category.Id)

        if export_types:
            collector.WhereElementIsElementType()
        else:
            collector.WhereElementIsNotElementType()

        elements.extend(collector.ToElements())

    parameter_names = select_parameters(elements) or script.exit()

    data['Parameters'] = parameter_names

    # logger.debug(elements_dict)

    element_data = get_element_parameter_values(elements, parameter_names)

    if get_extended_data:
        if builtin_category in (
                DB.BuiltInCategory.OST_Floors,
                DB.BuiltInCategory.OST_Walls,
                DB.BuiltInCategory.OST_Roofs,
                DB.BuiltInCategory.OST_Ceilings,
                ):

            for element in elements:
                compound_structure = element.GetCompoundStructure()
                if compound_structure:
                    element_data[element].update({
                        '~Layers': antler.parameters.compound_structure_summary(
                            compound_structure, sep='\r\n'),
                    })
                    element_data[element].update({
                        '~LayersShort': antler.parameters.compound_structure_summary(
                            compound_structure, sep='-', layer_string_function=antler.parameters.minimal_layer_string),
                    })
                if export_types:
                    instance_elements = antler.collectors.get_instances_of_element_type(element)
                    count = len(instance_elements)#.GetElementCount()

                    element_data[element].update({
                        '~Count': count
                    })

    data['Elements'] = element_data

    return data


def export_current_selection(
        export_types=False,
        # include_links=False,
        # count_elements=False,
        get_extended_data=False,
        **kwargs):

    current_selection = revit.uidoc.Selection.GetElementIds()

    elements = [revit.doc.GetElement(a) for a in current_selection]

    data = {}

    data['Header'] = "{type_or_instance} elements from {doc}".format(
        type_or_instance='Type' if export_types else "Instance",
        doc=revit.doc.Title
        )

    parameters = antler.parameters.get_all_parameters(
        # element_dict.keys(),
        elements,
        hashable_provider=antler.parameters.parameter_name_string_provider)

    parameter_selection = forms.SelectFromList.show(
        sorted(parameters),
        title='Select Parameters to Export',
        multiselect=True
    )

    data['Elements'] = get_element_parameter_values(elements, parameter_selection)
    data['Parameters'] = parameter_selection

    return data


def export_visible_elements(
        export_types=False,
        # include_links=False,
        # count_elements=False,
        get_extended_data=False,
        **kwargs):
    collector = DB.FilteredElementCollector(revit.doc, revit.uidoc.ActiveView.Id)

    if export_types:
        collector.WhereElementIsElementType()
    else:
        collector.WhereElementIsNotElementType()

    elements = collector.ToElements()

    data = {}

    data['Header'] = "{type_or_instance} elements from {view} in {doc}".format(
        type_or_instance='Type' if export_types else "Instance",
        view=revit.uidoc.ActiveView.Name,
        doc=revit.doc.Title
        )

    parameters = antler.parameters.get_all_parameters(
        # element_dict.keys(),
        elements,
        hashable_provider=antler.parameters.parameter_name_string_provider)

    parameter_selection = forms.SelectFromList.show(
        sorted(parameters),
        title='Select Parameters to Export',
        multiselect=True
    )

    data['Elements'] = get_element_parameter_values(elements, parameter_selection)
    data['Parameters'] = parameter_selection

    return data


def export_dict_list_to_csv(filename, dict_list, columns=[]):
    """
    """
    import unicodecsv as csv

    keys = set().union(*(d.keys() for d in dict_list))

    # System.IO.IOException
    with open(filename, mode='wb') as f:
        w = csv.DictWriter(f, keys, delimiter=';', quotechar='"',
                            quoting=csv.QUOTE_MINIMAL, )
        w.writeheader()

        for row in dict_list:
            w.writerow(row)


def export_dict_list_to_xlxs(
        filename, dict_list, columns=[]):
    """
    """
    import xlsxwriter

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    # keys = set().union(*(d.keys() for d in dict_list))

    headers, data = antler.util.dict_list_to_array(dict_list)

    # Write column headers
    worksheet.write_row(0, 0, headers)

    # Write row data
    for i, row in enumerate(data):
        worksheet.write_row(i+1, 0, row)

    workbook.close()


def interpret_existing_export(export_file):
    pass


logger = script.get_logger()
config = script.get_config()



choice_switch = {
    "Elements of Category": export_elements_of_category,
    "Elements of Multiple Categories": export_elements_of_categories,
    # "Elements in current View": export_elements_in_current_view,
    'Current Selection': export_current_selection,
    'Elements Visible in View': export_visible_elements,
    'Materials': export_materials,
}

# type_switch = {
#     'Types': True,
#     'Instance' False
# }

choice, switches = forms.CommandSwitchWindow.show(
    choice_switch.keys(),
    switches=['Types', 'Multiple Docs', 'Extended Data'],
    message="What do you want to export?"
)

if not choice:
    script.exit()


if switches['Multiple Docs']:
    docs = antler.forms.select_docs(
            selection_filter=lambda x: not x.IsFamilyDocument)
else:
    docs=[revit.doc]


data = choice_switch[choice](
    export_types=switches['Types'],
    include_links=switches['Multiple Docs'],
    get_extended_data=switches['Extended Data'],
    docs=docs
    )

# print(json.dumps(data, sort_keys=True, indent=4))

# for k, v in data.items():
#     logger.debug(k)
#     logger.debug(v)


antler.util.print_dict_list(data['Elements'].values())


selected_option = forms.alert(
    'Export table to file?',
    options=["Export", "Cancel"],
) or script.exit()

exporters_extension_mapping = {
    '.csv': export_dict_list_to_csv,
    '.xlsx': export_dict_list_to_xlxs
}


def save_to_config(data):
    parameter_names = []

    config_data = {
        category: parameter_names
    }


if selected_option == "Export":
    filename = data['Header'].replace(':', ' -')

    file_path = antler.forms.save_file_dialog(
        default_name=filename,
        filter={'csv': '*.csv', 'xlsx': '*.xlsx'}
    ) or script.exit()

    filename, extension = os.path.splitext(file_path)

    print(file_path)

    exporters_extension_mapping[extension](file_path, data['Elements'].values())

    # script.exit()
    #
    # export_dict_list_to_csv(file_path, data['Elements'].values())
