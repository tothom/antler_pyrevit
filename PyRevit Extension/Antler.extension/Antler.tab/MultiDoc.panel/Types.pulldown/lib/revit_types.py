from pyrevit import forms, script
from rpw import DB
import antler


# common_parameters = antler.parameters.get_common_parameters(list(elements_a) + list(elements_b), intersect_set=True)
def select_match_parameter(category, doc):
    parameters = antler.parameters.get_builtin_parameters_of_category(
        category, doc=doc)

    # parameters = antler.parameters.get_common_parameters_by_category(
    #     category, doc, hashable_provider=antler.parameters.parameter_name_string_provider)

    parameters = {k: v for k, v in parameters.items(
    ) if doc.get_TypeOfStorage(v) == DB.StorageType.String}

    match_parameter_name = forms.SelectFromList.show(
        sorted(parameters.keys()),
        title='Select Parameter for matching.',
        multiselect=False
    ) or script.exit()

    match_parameter = parameters[match_parameter_name]

    return match_parameter


def find_and_compare_elements(elements, destination_doc, match_parameter, **kwargs):
    diff = []

    for element in elements:
        # element_name = antler.parameters.get_element_name(element)

        other_element = antler.compare.find_similar_element(
            element, destination_doc, parameter=match_parameter)

        if other_element:
            # logger.info((
            #     antler.parameters.get_element_name(element),
            #     antler.parameters.get_element_name(other_element)))

            comparison = antler.compare.diff_elements(element, other_element, exceptions=kwargs['exceptions'])

            if comparison:
                # diff[(element, other_element)] = definitions
                diff.extend(comparison)

    return diff
