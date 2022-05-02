# -*- coding: utf-8 -*-
from rpw import revit, DB

from pyrevit import forms, script
# import clr
import re

# import antler

logger = script.get_logger()

workset_table = revit.doc.GetWorksetTable()

user_input = forms.ask_for_string(
    message="Workset names, separated by comma")

workset_names = [a.strip() for a in re.split('[;|,\r]', user_input)]

logger.debug(workset_names)

if not workset_names:
    script.exit()

decision = forms.CommandSwitchWindow.show(
    ['Ok', 'Abort'],
    message='This will create the worksets {}'.format(workset_names)
)

if not decision == 'Ok':
    script.exit()

with DB.Transaction(revit.doc, __commandname__) as tg:
    tg.Start()

    for workset_name in workset_names:
        try:
            DB.Workset.Create(revit.doc, workset_name)
        except Exception as e:
            logger.warning(e)
            logger.warning(workset_name)

    tg.Commit()
