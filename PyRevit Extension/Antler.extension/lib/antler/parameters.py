from rpw import revit, DB
from rpw.exceptions import RevitExceptions
from pyrevit import forms, script

import System.Enum
import clr

from System.Collections.Generic import List

logger = script.get_logger()


def get_element_id_parameter_as_name(parameter):
    """
    Just use AsValueString() instead??
    """
    # parameter_element = clr.Convert(parameter, DB.ParameterElement)
    doc = parameter.Element.Document

    element = doc.GetElement(parameter.AsElementId())

    logger.debug(element)

    if element:
        name_parameter = element.get_Parameter(
            DB.BuiltInParameter.ALL_MODEL_TYPE_NAME)

        return name_parameter.AsString()


def get_element_id_parameter_value_by_name(parameter, name):
    doc = parameter.Element.Document

    if parameter.Definition.ParameterType == DB.ParameterType.Material:
        material = collectors.get_material_by_name(name, doc)

        if material:
            return material.Id
        else:
            return None
            # raise KeyError("No material with name {} found.".format(name))



def get_parameter_value(parameter, convert=True, mapping_overrides={}):
    PARAMETER_GET_MAPPING = {
        DB.StorageType.Integer: DB.Parameter.AsInteger,
        DB.StorageType.Double: DB.Parameter.AsDouble,
        DB.StorageType.String: DB.Parameter.AsString,
        DB.StorageType.ElementId: DB.Parameter.AsElementId,
    }

    PARAMETER_GET_MAPPING.update(mapping_overrides)

    logger.debug("Definition Name: {}".format(parameter.Definition.Name))
    logger.debug("Parameter Type: {}".format(parameter.Definition.ParameterType))
    logger.debug("Storage Type: {}".format(parameter.StorageType))
    logger.debug("AsValueString: {}".format(parameter.AsValueString()))

    if not parameter.HasValue:
        return

    # if parameter.Definition.ParameterType == DB.ParameterType.Invalid:
    #     internal_value = parameter.AsValueString()
    # else:
    internal_value = PARAMETER_GET_MAPPING.get(
        parameter.StorageType, DB.Parameter.AsValueString)(parameter)
        # internal_value = PARAMETER_GET_MAPPING[parameter.StorageType](parameter)

    logger.debug("Internal value: {}".format(internal_value))

    if convert:
        try:
            value = DB.UnitUtils.ConvertFromInternalUnits(
                internal_value, parameter.DisplayUnitType)
        except RevitExceptions.InvalidOperationException as e:
            # logger.warning((type(e), e))
            value = internal_value

        return value

    else:
        return internal_value


def set_parameter_value(parameter, value, convert=True, mapping_overrides={}):
    PARAMETER_SET_MAPPING = {
        DB.StorageType.Integer: int,
        DB.StorageType.Double: float,
        DB.StorageType.String: str,
        DB.StorageType.ElementId: DB.ElementId,
    }

    PARAMETER_SET_MAPPING.update(mapping_overrides)

    value = PARAMETER_SET_MAPPING[parameter.StorageType](value)

    if convert:
        try:
            internal_value = DB.UnitUtils.ConvertToInternalUnits(
                value, parameter.DisplayUnitType)
        except RevitExceptions.InvalidOperationException as e:
            # logger.warning((type(e), e))
            internal_value = value
        parameter.Set(internal_value)

    else:
        parameter.Set(value)


def reset_parameter_value(parameter):
    parameter.Set(DB.ElementId.InvalidElementId)


def query_parameter(parameter):
    query = {
        'Name': parameter.Definition.Name,
        'Id': parameter.Id,
        'IsShared': parameter.IsShared,
        'GUID': parameter.GUID,
    }

    return query


def get_builtin_parameter_from_id(parameter_id):
    for builtin_parameter in System.Enum.GetValues(DB.BuiltInParameter):
        if DB.ElementId(builtin_parameter).IntegerValue == parameter_id.IntegerValue:
            return builtin_parameter


def parameter_is_equivalent(parameter_a, parameter_b):
    # First test - Name must be equal

    logger.info("")

    # if parameter_a.Definition.Name != parameter_b.Definition.Name:
    #     return False

    try:
        internal_definition_a = clr.Convert(
            parameter_a.Definition, DB.InternalDefinition)
        internal_definition_b = clr.Convert(
            parameter_b.Definition, DB.InternalDefinition)
    except Exception as e:
        logger.warning(e)
    else:
        builtin_parameter_a = internal_definition_a.BuiltInParameter
        builtin_parameter_b = internal_definition_b.BuiltInParameter

        return builtin_parameter_a == builtin_parameter_b

    try:
        external_definition_a = clr.Convert(
            parameter_a.Definition, DB.ExternalDefinition)
        external_definition_a = clr.Convert(
            parameter_a.Definition, DB.ExternalDefinition)
    except Exception as e:
        logger.warning(e)
    else:
        guid_a = external_definition_a.GUID
        guid_b = external_definition_b.GUID

        return guid_a == guid_b

    return False


def parameter_identifier_provider(parameter):
    if parameter.IsShared:
        return parameter.GUID
    else:
        definition = parameter.Definition
        internal_definition = clr.Convert(definition, DB.InternalDefinition)

        if internal_definition.BuiltInParameter != DB.BuiltInParameter.INVALID:
            return internal_definition.BuiltInParameter
        else:
            return definition


def parameter_string_identifier_provider(parameter):
    """
    Gets a unique string identifying the input parameter.
    """
    logger.debug(parameter)
    # logger.debug(parameter.GetDefinition())
    logger.debug(type(parameter))

    if isinstance(parameter, DB.BuiltInParameter):
        identifier = parameter
        key = "{name} ({builtin})".format(
            name=DB.LabelUtils.GetLabelFor(parameter),
            builtin=parameter
        )
    elif isinstance(parameter, DB.SharedParameterElement):
        identifier = parameter.GuidValue
        key = "{name} ({guid})".format(
            name=parameter.GetDefinition().Name,
            guid=parameter.GuidValue
        )
    elif isinstance(parameter, DB.ParameterElement):
        definition = parameter.GetDefinition()
        identifier = (
            definition.Name,
            definition. ParameterType
        )
        key = "{name} ({param_type})".format(
            name=definition.Name,
            param_type=DB.LabelUtils.GetLabelFor(definition.ParameterType)
        )
    elif isinstance(parameter, DB.Parameter):
        try:
            key = "{} ({})".format(
                parameter.Definition.Name,
                DB.LabelUtils.GetLabelFor(parameter.Definition.ParameterGroup)
            )
            return key
        except:
            return None

    return key




def parameter_name_string_provider(parameter):
    if isinstance(parameter, DB.BuiltInParameter):
        return DB.LabelUtils.GetLabelFor(parameter)
    else:
        return parameter.Definition.Name



def get_all_parameters(
    elements,
    filter_function=lambda x: True,
    hashable_provider=parameter_identifier_provider,
    parameters_provider=lambda x:x.Parameters,
    # get_common_parameters=False
):
    """
    """
    element_parameter_set = set()
    # element_parameter_dict = {}

    for element in elements:
        for parameter in parameters_provider(element):
            if filter_function(parameter):
                hashable = hashable_provider(parameter)
                element_parameter_set.add(hashable)
    #             element_parameter_dict[hashable] = parameter.Id
    #
    # return element_parameter_dict
    return list(element_parameter_set)


def get_all_definitions(
    elements,
    filter_function=lambda x: True,
    hashable_provider=parameter_string_identifier_provider,
    parameters_provider=lambda x:x.Parameters,
    # get_common_parameters=False
    ):
    """
    """
    element_parameter_dict = {}

    for element in elements:
        for parameter in parameters_provider(element):
            if filter_function(parameter):
                hashable = hashable_provider(parameter)

                if hashable:
                    element_parameter_dict[hashable] = parameter.Definition

    return element_parameter_dict




def get_all_parameter_names(
    elements,
    filter_function=lambda x: True,
    parameters_provider=lambda x:x.Parameters,
    # get_common_parameters=False
):
    """
    """
    element_parameter_set = set()

    for element in elements:
        for parameter in parameters_provider(element):
            if filter_function(parameter):
                hashable = parameter_name_string_provider(parameter)
                element_parameter_set.add(hashable)

    return list(element_parameter_set)


def get_definitions_from_elements(
        elements,
        filter_function=lambda x: True,
        hashable_provider=parameter_identifier_provider,
        parameters_provider=lambda x:x.Parameters,
        intersect_set=True
):
    """
    """
    hashable_list_of_lists = []
    definitions_dict = {}

    for element in elements:
        hashable_set = set()

        for parameter in parameters_provider(element):
            if filter_function(parameter):
                hashable = hashable_provider(parameter)

                hashable_set.add(hashable)
                definitions_dict[hashable] = parameter.Definition

        hashable_list_of_lists.append(hashable_set)

    if intersect_set:
        keys = set.intersection(*hashable_list_of_lists)
    else:
        keys = set.union(*hashable_list_of_lists)

    return [definitions_dict[k] for k in keys]



def get_common_parameters_by_category(category, doc=revit.doc, hashable_provider=parameter_name_string_provider,):
    common_parameters = DB.ParameterFilterUtilities.GetFilterableParametersInCommon(
        doc, List[DB.ElementId]([category.Id]))

    parameter_identifiers_dict = {}

    for parameter_id in common_parameters:
        logger.info(parameter_id)

        # parameter = [a for a in DB.Built]

        # parameter = doc.GetElement(parameter_id)
        parameter = get_builtin_parameter_from_id(
            parameter_id)

        if not parameter:
            parameter = doc.GetElement(parameter_id)

        logger.info(parameter)

        identifier = hashable_provider(parameter)

        parameter_identifiers_dict[identifier] = parameter

    logger.info(parameter_identifiers_dict.items())

    return parameter_identifiers_dict

def get_builtin_parameters_of_category(category, doc=revit.doc):
    common_parameters = DB.ParameterFilterUtilities.GetFilterableParametersInCommon(
        doc, List[DB.ElementId]([category.Id]))

    parameter_dict = {}

    for parameter_id in common_parameters:
        parameter = get_builtin_parameter_from_id(
            parameter_id)

        if not parameter:
            continue
        else:
            parameter_dict[DB.LabelUtils.GetLabelFor(parameter)] = parameter

    return parameter_dict

def verbose_layer_string(layer):
    logger.debug(layer)

    material = revit.doc.GetElement(layer.MaterialId)

    logger.debug(material)

    if material:
        material_name = material.Name
    else:
        material_name = "*By Category*"

    layer_string = "{width} - {material_name}".format(
        function=layer.Function,
        # width=layer.Width*304.8,
        width=DB.UnitFormatUtils.Format(
                        revit.doc.GetUnits(),
                        DB.SpecTypeId.Length,
                        layer.Width,
                        False),
        material_name=material_name
    )

    return layer_string


def minimal_layer_string(layer):
    # for parameter in layer.Parameters:
    #     logger.debug("{parameter}: {value}".format(
    #         parameter=parameter.Definition.Name,
    #         value=get_parameter_value(parameter)
    #     ))

    layer_string = "{width}".format(
        width=DB.UnitFormatUtils.Format(
            revit.doc.GetUnits(),
            DB.SpecTypeId.Length,
            layer.Width,
            False),
    )

    return layer_string


def compound_structure_summary(
        compound_structure,
        sep='; ',
        layer_string_function=verbose_layer_string):

    layer_string_list = []

    for layer in compound_structure.GetLayers():
        layer_string = layer_string_function(layer)

        layer_string_list.append(layer_string)

    compound_string = sep.join(layer_string_list)

    return compound_string


def get_element_name(element):
    try:
        return element.Name
    except:
        parameter = element.get_Parameter(
            DB.BuiltInParameter.ALL_MODEL_TYPE_NAME)

        return parameter.AsString()
