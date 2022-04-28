import antler
from pyrevit import script

logger = script.get_logger()


def override_color_by_parameter(view, element, parameter):
    try:
        element_parameter = element.get_Parameter(parameter)
        # parameter_value = antler.parameters.get_parameter_value(element_parameter, convert=True)

        # Seems to be most consistent as seed value.
        parameter_value = element_parameter.AsValueString()
    except Exception as e:
        logger.debug(type(e))
        logger.debug(e)
        parameter_value = None

    logger.debug(parameter_value)

    if parameter_value is not None:
        line_color = antler.color.random_hsv_color(
            seed=parameter_value, s=0.8, v=0.6)

        fill_color = antler.color.relative_color_hsv(line_color, dv=+0.3)

        logger.debug(line_color)
        logger.debug(fill_color)

        antler.view.override_element_color(
            element, view, fill_color=fill_color, line_color=line_color)
    else:
        antler.view.override_element_color(
            element, view)
