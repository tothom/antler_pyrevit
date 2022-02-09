from rpw import revit, DB
from rpw.exceptions import RevitExceptions
from pyrevit import forms, script

logger = script.get_logger()


def get_parameter_value(parameter, convert=True):
    PARAMETER_GET_MAPPING = {
        DB.StorageType.Integer: DB.Parameter.AsInteger,
        DB.StorageType.Double: DB.Parameter.AsDouble,
        DB.StorageType.String: DB.Parameter.AsString,
        DB.StorageType.ElementId: DB.Parameter.AsElementId,
    }

    logger.debug(parameter.Definition.Name)
    logger.debug(parameter.StorageType)

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


def set_parameter_value(parameter, value, convert=True):
    PARAMETER_SET_MAPPING = {
        DB.StorageType.Integer: int,
        DB.StorageType.Double: float,
        DB.StorageType.String: str,
        DB.StorageType.ElementId: DB.ElementId,
    }

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
    # if not parameter.IsReadOnly:



def get_common_parameter_definitions(elements, filter_function=lambda x:True):
    """
    Returns common parameter definitions for input elements. Example if all
    elements has a parameter for Area, the Area parameter definition will be
    returned.

    The filter function takes the parameter as argument.
    """
    valid_definition_sets = []
    valid_definitions_dict = {}

    for element in elements:
        valid_definition_set = set()

        for parameter in element.Parameters:

            logger.debug("Checking {definition}: {storage_type}".format(
                definition=parameter.Definition.Name,
                storage_type=parameter.StorageType
            ))

            if filter_function(parameter):
                valid_definition_set.add(parameter.Definition.Id)
                valid_definitions_dict[parameter.Definition.Id] = parameter.Definition

                logger.debug("Definition {definition} add to set.".format(
                    definition=parameter.Definition.Name))

        valid_definition_sets.append(valid_definition_set)

    logger.debug(valid_definition_sets)

    common_parameter_definitions = [valid_definitions_dict[id] for id in set.intersection(*valid_definition_sets)]

    return list(common_parameter_definitions)
