# from System.Collections.Generic import *
from rpw import revit, DB, UI
from pyrevit import forms, script, EXEC_PARAMS

import antler
import antler_revit

logger = script.get_logger()


def assure_parameter_visibility_settings_in_type(doc):
    manager = doc.FamilyManager
    types = manager.Types

    iterator = types.ForwardIterator()
    iterator.Reset()

    i = 0

    while iterator.MoveNext():# and i < 10:
        family_type = iterator.Current
        logger.info("Family Type: " + family_type.Name)

        with DB.Transaction(doc, "Set parameter visibility") as t:
            t.Start()
            manager.CurrentType = family_type

            # Code for whatever you want to do.
            parameters = manager.GetParameters()

            for parameter in parameters:

                if parameter.Definition.ParameterType == DB.ParameterType.YesNo \
                    and parameter.Definition.ParameterGroup == DB.BuiltInParameterGroup.PG_VISIBILITY:
                        #pass
                        #
                        if parameter.Definition.Name == family_type.Name:
                            logger.info("Parameter: " + parameter.Definition.Name)
                            manager.Set(parameter, 1)
                        # else:
                        #manager.Set(parameter, 0)

            t.Commit()
            # t.Dispose()


        logger.info(i)
        i += 1
        # End Transaction
        #TransactionManager.Instance.TransactionTaskDone()

# Place your code below this line
with DB.TransactionGroup(revit.doc, __commandname__) as tg:
    tg.Start()

    assure_parameter_visibility_settings_in_type(revit.doc)
    # tg.Assimilate()
    tg.Commit()
