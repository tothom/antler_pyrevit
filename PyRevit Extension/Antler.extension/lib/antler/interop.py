from rpw import revit, DB
import json

from pyrevit import script
logger = script.get_logger()

class Serializer():
    """
    Should use RPW to serialize parameters...? https://revitpythonwrapper.readthedocs.io/en/latest/db/element.html
    """
    pass

def lookup_parameters(element, include_parameters=None):
    """
    Returns all parameters of element, unless parameters are provided in include_parameters. Parameters can be provided as Parameter, Definition or as a string.

    # TODO: Deprecate function?
    """
    # print(include_parameters)
    parameters = []

    if not include_parameters:
        parameters = element.Parameters
    else:
        for a in include_parameters:
            # print(type(a))
            if isinstance(a, basestring):
                parameter = element.LookupParameter(a)
            elif isinstance(a, [DB.Parameter, DB.Definition]):
                parameter = element.get_Parameter(a)

            parameters.append(parameter)

    logger.debug(parameters)

    return parameters



def element_to_dict(element):
    parameters = lookup_parameters(element)

    parameter_dict = {}

    for parameter in parameters:
        key = parameter.Definition.Name
        value = parameter.AsString() or parameter.AsValueString()

        parameter_dict[key] = value

    return parameter_dict

def family_symbol_to_dict(family_symbol, include_parameters=None, doc=revit.doc):
    """
    """
    parameters = lookup_parameters(family_symbol, include_parameters)

    parameter_dict = {}

    for parameter in parameters:
        key = parameter.Definition.Name
        value = parameter.AsString() or parameter.AsValueString()

        parameter_dict[key] = value

    return parameter_dict


def family_to_dict(family, include_parameters=None, doc=revit.doc):
    """
    Returns a nested dictionary of all Types in Family with corresponding Parameters and values.
    """
    family_symbols = []

    for symbol_id in family.GetFamilySymbolIds():
        family_symbol_element = doc.GetElement(symbol_id)

        family_symbols.append(family_symbol_to_dict(family_symbol_element))

    return family_symbols

def material_to_dict(material, include_parameters=None, doc=revit.doc):
    pass


def compound_structure_to_dict(compound_structure):
    layers_dict = {}

    for layer in compound_structure.GetLayers():
        material_id = layer.MaterialId
        material = revit.doc.GetElement(material_id)

        material_dict = {}

        if material:
            material_dict = element_to_dict(material)

        layers_dict[layer.LayerId] = {
            'Function': layer.Function,
            'Width': layer.Width,
            'Material Id': layer.MaterialId.IntegerValue,
            'Material': material_dict,
            }

    return layers_dict

def room_to_dict(room):
    pass
    # ID: Room Number

    # Properties: Name, area, level,

    # Get connected rooms
