from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms
from collections import OrderedDict

import re

__doc__ = "Search and replace view names"
__title__ = "Search and Replace\nView Names"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc

regex_pattern = forms.ask_for_string(
    prompt="Enter regex search pattern. Groups are not supported.",
    title="Regex pattern"
)

replace_text = forms.ask_for_string(
    prompt="Enter replacement text",
    title="Replacement text"
)

# replace_text = "%r"%replace_text[1:-1]
# print(replace_text)

# regex_pattern_compiled = re.compile(regex_pattern)
# replace_text_compiled = re.compile(replace_text)

# regex_pattern = regex_pattern.encode('string-escape')
# replace_text = replace_text.encode('string-escape')

if uidoc.Selection.GetElementIds():
    views = [doc.GetElement(id) for id in uidoc.Selection.GetElementIds()]
else:
    views = forms.select_views()

if views and replace_text is not None:
    with DB.Transaction(doc, __title__) as t:
        t.Start()

        for view in views:
            view.Name = re.sub(regex_pattern, replace_text, view.Name)

        t.Commit()
