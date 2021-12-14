from rpw import revit, DB


def ifc_guid_filter(guid):
    ifc_param = DB.BuiltInParameter.IFC_GUID

    pvp = DB.ParameterValueProvider(DB.ElementId(ifc_param))
    filter_rule = DB.FilterStringRule(
        pvp, DB.FilterStringContains(), guid, False)
    epf = DB.ElementParameterFilter(filter_rule)

    return epf


def hosted_by_filter(host_element):
    """
    """
    provider = DB.ParameterValueProvider(DB.ElementId(DB.BuiltInParameter.HOST_ID_PARAM))
    rule = DB.FilterElementIdRule(provider, DB.FilterNumericEquals(), host_element.Id)
    parameter_filter = DB.ElementParameterFilter(rule)

    return parameter_filter
