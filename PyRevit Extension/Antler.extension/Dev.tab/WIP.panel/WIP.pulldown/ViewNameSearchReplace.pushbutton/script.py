from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms
from collections import OrderedDict

import re

__doc__ = "Autorename views"
__title__ = "Rename Views"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc



"""
rename_dict = {
    "ARK stair 02":   "B 01 Adkomst",
    "ARK_stair 02":   "B 01 Adkomst",
    "ARKstair 02":   "B 01 Adkomst",
                    : "A 01 Adkomst"
                    : "A U1 Teknisk etg"
                    : "A U2 Teknisk etg"
                    : "A U3 Teknisk etg"
                    : "A U4 Teknisk etg"
                    : "A U5 Platform"
                    : "U6"
                    : "B 01 Adkomst"
                    : "B U1 Teknisk etg"
                    : "B U2 Adkomsthall"
                    : "B U3 Teknisk etg"
                    : "B U4 Teknisk etg"
                    : "B U5 Plattform"
    }
"""



import os
file_path = os.path.join(__commandpath__, 'regex_pattern.txt')

with open(file_path, 'w+') as f:
    regex_pattern = f.read()

    # print(regex_pattern)

    regex_pattern = forms.ask_for_string(
        default=regex_pattern,
        prompt="Enter regex search pattern",
        title="Regex pattern"
    )

    # regex_pattern = "(?i)ARK[ _]*stair\s*\d*\.*\d*"
    f.write(regex_pattern)

regex_pattern_compiled = re.compile(regex_pattern)

# views = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
if uidoc.Selection.GetElementIds():
    views = [doc.GetElement(id) for id in uidoc.Selection.GetElementIds()]
else:
    views = forms.select_views()

if views:
    with DB.Transaction(doc, __title__) as t:
        t.Start()

        for view in views:
            match = re.search(regex_pattern_compiled, view.Name)

            # print(view.Name)
            # print(match.group())
            # print(view.Name[:match.start()] + view.Name[match.end():])
            try:
                view.Name = view.Name[:match.start()] + view.Name[match.end():]
            except Exception as e:
                print(e)
            # level = view.GenLevel
            # if level:
            #     view.Name = "{0} - {1}".format(view.Name, level.Name)

            # print(element)
            # builtin_parameters = builtin_parameter_mapping.get(type(element))
            #
            # if not builtin_parameters:
            #     print("{} not yet supported".format(type(element)))

        t.Commit()

with open(file_path, 'w') as f:

    f.write(regex_pattern)
