# -*- coding: utf-8 -*-

from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms
from collections import OrderedDict

import os
import csv
import json


# https://www.revitapidocs.com/2021.1/5b944368-4ce5-d523-5fd5-29d0363861ae.htm
revit_link_type = DB.RevitLinkType.CreateFromIFC(revit.doc, ifcFilePath, revitLinkedFilePath, recreateLink, RevitLinkOptions)


import_placement = DB.ImportPlacement.Site #, Origin, Center, Shared

RevitLinkInstance = DB.RevitLinkInstance.Create(doc, linkTypeId, import_placement)
