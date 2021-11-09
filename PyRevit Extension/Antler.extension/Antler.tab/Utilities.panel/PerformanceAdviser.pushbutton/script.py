# -*- coding: utf-8 -*-
from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script
from collections import OrderedDict

import sys


__doc__ = "Execute performance adviser rules"
__title__ = "Performance Adviser"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

logger = script.get_logger()

adviser = DB.PerformanceAdviser.GetPerformanceAdviser()

rule_ids = adviser.GetAllRuleIds()

rule_dict = OrderedDict()

for id in rule_ids:
    name = adviser.GetRuleName(id)
    description = adviser.GetRuleDescription(id)

    rule_dict[name] = (description, id)

selected_rules = forms.SelectFromList.show(
    sorted(rule_dict.keys()),
    title="Select performance tests to execute.",
    multiselect=True
    )

rules_to_execute = List[DB.PerformanceAdviserRuleId](
    [rule_dict[a][1] for a in selected_rules])

failures = adviser.ExecuteRules(doc, rules_to_execute)

logger.debug(failures)

if not failures:
    print("No problems found! 👌")
else:
    with DB.Transaction(doc, __title__) as t:
        t.Start()
        for failure in failures:
            doc.PostFailure(failure)
        t.Commit()
