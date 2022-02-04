from rpw import revit, DB
from rpw.exceptions import RevitExceptions
from pyrevit import forms, script

logger = script.get_logger()


def get_parameter_value(parameter):
    PARAMETER_GET_MAPPING = {
        DB.StorageType.Integer: DB.Parameter.AsInteger,
        DB.StorageType.Double: DB.Parameter.AsDouble,
        DB.StorageType.String: DB.Parameter.AsString,
        DB.StorageType.ElementId: DB.Parameter.AsElementId,
    }

    internal_value = PARAMETER_GET_MAPPING[parameter.StorageType](parameter)

    try:
        value = DB.UnitUtils.ConvertFromInternalUnits(
            internal_value, parameter.DisplayUnitType)
    except RevitExceptions.InvalidOperationException as e:
        # logger.warning((type(e), e))
        value = internal_value

    return value


def set_parameter_value(parameter, value):
    PARAMETER_SET_MAPPING = {
        DB.StorageType.Integer: int,
        DB.StorageType.Double: float,
        DB.StorageType.String: str,
        DB.StorageType.ElementId: DB.ElementId,
    }

    value = PARAMETER_SET_MAPPING[parameter.StorageType](value)

    try:
        internal_value = DB.UnitUtils.ConvertToInternalUnits(
            value, parameter.DisplayUnitType)
    except RevitExceptions.InvalidOperationException as e:
        # logger.warning((type(e), e))
        internal_value = value

    # if not parameter.IsReadOnly:
    parameter.Set(internal_value)


def get_common_parameters(elements):
    common_parameters = []
    pass
