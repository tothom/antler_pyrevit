# -*- coding: utf-8 -*-

from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms, script, EXEC_PARAMS
from collections import OrderedDict, defaultdict

import os
# import csv
import unicodecsv as csv
# import xml.etree.ElementTree as ET
# from xml import etree
from io import StringIO, BytesIO
import lxml# import etree
import re

import antler

logger = script.get_logger()
output = script.get_output()


def import_html(data):
    # interpreted_data = {}
    structured_data = defaultdict(dict)

    structured_data[doc].update({element: parameter_dict})

    return structured_data


# Open and read CSV
file = forms.pick_file(file_ext='html') or script.exit()


with open(file, mode='r') as f:
    logger.info(f)
    logger.info(dir(lxml))
    text = f.read()
    #
    # parser = ET.XMLParser(recover=True, encoding='utf-8')
    # tree   = ET.parse(StringIO(text), parser)
    # # tree = ET.parse(f)
    # # tree = ET.fromstring(text, encoding='utf-8')
    # # root = tree.getroot()
    #
    # logger.info(tree)


    # data = import_html(import_list)
