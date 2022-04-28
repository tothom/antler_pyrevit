# -*- coding: utf-8 -*-

from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

from System.Collections.Generic import List

import antler

logger = script.get_logger()
output = script.get_output()

category = antler.forms.select_category() or script.exit()



element_types = antler.forms.select_types_of_category(
    categories=[category], count_elements=True) or script.exit()



with DB.Transaction(revit.doc, "Delete Element Types") as t:
    t.Start()

    for element_type in element_types:
        # link = output.linkify(element_type.Id)
        name = DB.Element.Name.GetValue(element_type)

        try:
            deleted_id_set = revit.doc.Delete(element_type.Id)
        except Exception as e:
            logger.warning(e)
            output.print_md("Element **{element}** NOT deleted.".format(
                element=name
            ))
        else:
            output.print_md("Element **{element}** deleted.".format(
                element=name
            ))

    t.Commit()

    # tg.Assimilate()
