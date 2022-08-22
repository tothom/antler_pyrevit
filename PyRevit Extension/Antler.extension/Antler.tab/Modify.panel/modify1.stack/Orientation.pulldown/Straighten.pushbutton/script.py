# from System.Collections.Generic import *
from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

import antler
import antler_revit
import math
# import clr

from System.Drawing import Color  # noqa: E402


ANGLE_TOLERANCE = 1e-14

logger = script.get_logger()
config = script.get_config()
output = script.get_output()

def select_guides():
    global guide_ids
    references = uidoc.Selection.PickObjects(
        UI.Selection.ObjectType.Element, "Select objects to act as guides...")
    # except Autodesk.Revit.Exceptions.OperationCanceledException:
    #     script.exit()

    guide_ids = []

    for ref in references:
        # Only elements where direction can be extracted are included.
        if antler.geometry.transform.element_direction(doc.GetElement(ref)):
            guide_ids.append(ref.ElementId)

    if not guide_ids:
        logger.error("No valid guide elements selected")
        return

    config.guide_ids = [id.IntegerValue for id in guide_ids]

def set_angle_snap():
    global config

    angle_snap = forms.CommandSwitchWindow.show(
        [15, 30, 45, 60, 90],
        message='Snap angle. ESC for no additional angle snapping.'
    )

    config.angle_snap = angle_snap

    configure() # Go back to configure menu


def configure():
    choice_switch = {
        "Orient to View": None,
        # "Orient to Project North": None,
        # "Orient to True North": None,
        # "Orient to nearest grid": None,
        "Orient to guide objects", None,
        "Correct angle to decimal", None,
        "Orient to custom angle", None,
        "Set angle snap options", set_angle_snap
    }

    choice = forms.CommandSwitchWindow.show(
        choice_switch.keys(),
        message="What do you want to orient to?"
    ) or script.exit()


    script.save_config()

def get_orientation_color(angle)
    modulus = math.pi / 2.0
    hue = (angle % modulus) / modulus
    r, g, b = antler.color.hsv_to_rgb(hue, 0.8, 0.6)

    # modulus = math.pi / 1.0
    # seed = (angle_to_up % modulus) / modulus
    # line_color = antler.color.random_hsv_color(
    # 	seed=seed, s=0.7, v=0.7)

    return Color.FromArgb(
        int(r * 255), int(g * 255), int(b * 255))


# Select Elements
selection = revit.uidoc.Selection.GetElementIds() or revit.uidoc.Selection.PickObjects(
    UI.Selection.ObjectType.Element, "Select objects to check orientation...")

elements = [doc.GetElement(id) for id in selection]

# Config mode
if EXEC_PARAMS.config_mode:
    configure(config)

# check_orientation

# correct_orientation

with DB.Transaction(revit.doc, __commandname__) as t:
    t.Start()

    report = []

    for element in elements:
        element_report = {}

        element_report['Element'] = output.linkify(element.Id)

        #print("Checking element {element}".format(element=element_link))

        direction = antler.geometry.transform.element_direction(element)

        if direction is None:
            continue

        element_report['Angle To View Up'] = direction.AngleOnPlaneTo(
            revit.uidoc.ActiveView.UpDirection, DB.XYZ.BasisZ) / math.pi * 180.0 % 180.0

        element_report['Angle To Project North'] = direction.AngleOnPlaneTo(
            revit.uidoc.ActiveView.UpDirection, DB.XYZ.BasisZ) / math.pi * 180.0 % 180.0

        report.append(element_report)

        if EXEC_PARAMS.config_mode:
            color = get_orientation_color()

            antler.views.override_element_color(
                element,
                revit.uidoc.ActiveView,
                fill_color=antler.color.relative_color_hsv(color, dv=+0.2),
                line_color=color
                )

        # print(math.tan(angle_to_right))
        # print(math.tan(angle_to_up))
    t.Commit()

antler_revit.utils.print_dict_list(
    report, columns=['Element', 'Angle To View Up', 'Angle To Project North'])
