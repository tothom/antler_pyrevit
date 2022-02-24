from System.Collections.Generic import *
from rpw import revit, DB, UI

import os
from pathlib import Path
import re

import jalla

def get_extension_path():
    """
    Returns path of pyrevit extension
    """
    extension_pattern = '.extension\\'

    return __commandpath__.split(extension_pattern)[0] + extension_pattern

extension_path = get_extension_path()

extension_path = __commandpath__.split('.extension\\')[0] + '.extension\\'

lib_path = __commandpath__.split('.extension\\')[0] + '\\lib'

print(lib_path)

print(extension_path)

cmd_path = Path(__commandpath__)

# ext_path = cmd_path.relative_to('/*.extension')

#
lib_path  = re.split('\w*\.extension', __commandpath__)[0] + 'lib'
print(lib_path)


# Log write test
print(__commandpath__      )    # main script path
print(__configcommandpath__)    # config script path
print(__commandname__      )    # command name
print(__commandbundle__    )    # command bundle name
print(__commandextension__ )    # command bundle name
print(__commanduniqueid__  )    # command bundle name
print(__commandcontrolid__ )    # command control id
