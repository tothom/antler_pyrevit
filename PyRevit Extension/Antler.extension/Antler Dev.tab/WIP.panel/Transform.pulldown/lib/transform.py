from System.Collections.Generic import List
from rpw import revit, DB, UI
from pyrevit import forms, script


def relative_transform(from_transform, to_transform):
    pass


def set_transform(element, transform):
    element_transform = element.GetTotalTransform()

    relative_transform = relative_transform(element_transform, transform)

    scale = None
    rotation = None
    translation = None

    with DB.Transaction(doc, __commandname__) as t:
        t.Start()

        t.Commit()

def get_project_transforms(doc=revit.doc):
    pass


def set_position():
    pass
