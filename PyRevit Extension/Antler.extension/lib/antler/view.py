
from rpw import revit, DB

def query_view(view):
    pass


def override_element_color(element, view, fill_color=None, line_color=None):
    """
    Overrides color of element in view with input colors. The element will get
    a solid background fill in both cut and projection.

    If not color arguments are left empty, the element will get it's overrides removed.
    """
    # Get solid fill pattern
    solid_fill = DB.FillPatternElement.GetFillPatternElementByName(
        revit.doc, DB.FillPatternTarget.Drafting, "<Solid fill>")

    #create graphic overrides properties
    graphic_settings = DB.OverrideGraphicSettings()

    if fill_color is not None:
        fill_color = DB.Color(fill_color.R, fill_color.G, fill_color.B)
        # fill_color = dscolor_to_rcolor(ds_fill_colors[i])

        # Sets projection overrides
        graphic_settings.SetSurfaceBackgroundPatternId(solid_fill.Id)
        graphic_settings.SetSurfaceBackgroundPatternColor(fill_color)

        # Sets cut overrides
        graphic_settings.SetCutBackgroundPatternId(solid_fill.Id)
        graphic_settings.SetCutBackgroundPatternColor(fill_color)

    if line_color is not None:
        line_color = DB.Color(line_color.R, line_color.G, line_color.B)

        # line_color = dscolor_to_rcolor(ds_line_colors[i])
        # Sets projection overrides
        graphic_settings.SetProjectionLineColor(line_color)

        # Sets cut overrides
        graphic_settings.SetCutLineColor(line_color)

        graphic_settings.SetSurfaceForegroundPatternColor(line_color)
        graphic_settings.SetCutForegroundPatternColor(line_color)

    view.SetElementOverrides(element.Id, graphic_settings)
