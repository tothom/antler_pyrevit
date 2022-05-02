from rpw import revit, DB, UI


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
    provider = DB.ParameterValueProvider(
        DB.ElementId(DB.BuiltInParameter.HOST_ID_PARAM))
    rule = DB.FilterElementIdRule(
        provider, DB.FilterNumericEquals(), host_element.Id)
    parameter_filter = DB.ElementParameterFilter(rule)

    return parameter_filter


def room_phase_filter(phase):
    phase_id = phase.Id

    provider = DB.ParameterValueProvider(
        DB.ElementId(DB.BuiltInParameter.ROOM_PHASE_ID))
    rule = DB.FilterElementIdRule(provider, DB.FilterNumericEquals(), phase_id)
    parameter_filter = DB.ElementParameterFilter(rule)

    return parameter_filter


def view_name_filter(view_name):
    provider = DB.ParameterValueProvider(
        DB.ElementId(DB.BuiltInParameter.VIEW_NAME))
    rule = DB.FilterStringRule(
        provider, DB.FilterStringEquals(), view_name, False)
    parameter_filter = DB.ElementParameterFilter(rule)

    return parameter_filter


def category_name_filter(category_name):
    class category_name_filter(UI.Selection.ISelectionFilter):
        def AllowElement(self, element):
            if element.Category.Name == category_name:
                return True
            else:
                return False

        def AllowReference(self, ref, pt):
            return True

    return category_name_filter()
